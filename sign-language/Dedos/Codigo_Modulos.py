# Importar librerías necesarias
from ultralytics import YOLO
import depthai as dai
import cv2
import time
from collections import deque
from statistics import mode
import tkinter as tk
import paho.mqtt.client as mqtt
import threading

# =========================== Configuración MQTT =========================== #
broker = "broker.emqx.io"
puerto = 8883

# Función de conexión al broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
    else:
        print(f"Conexión fallida, código de error {rc}")

# Crear cliente MQTT y configurar TLS
client = mqtt.Client()
client.tls_set()
client.on_connect = on_connect
client.connect(broker, puerto)
client.loop_start()

# Función para publicar un mensaje a un tópico
def publicar(topico, mensaje):
    client.publish(topico, mensaje)
    print(f"Mensaje '{mensaje}' enviado al tópico '{topico}'")

# ======================== Interfaz Gráfica (Tkinter) ======================== #
# Función para actualizar la ventana con la frase final
def actualizar_frase_final(frase, topico, mensaje):
    frase_label.config(text=f"Frase Final: {frase}")
    topico_label.config(text=f"Tópico: {topico}")
    mensaje_label.config(text=f"Mensaje: {mensaje}")
    root.update_idletasks()

# Inicializar ventana de Tkinter
root = tk.Tk()
root.title("Frase Final")
root.geometry("400x200")

# Crear etiquetas para la ventana
frase_label = tk.Label(root, text="Frase Final: ", font=("Arial", 16))
frase_label.pack(pady=20)
topico_label = tk.Label(root, text="Tópico: ", font=("Arial", 12))
topico_label.pack(pady=5)
mensaje_label = tk.Label(root, text="Mensaje: ", font=("Arial", 12))
mensaje_label.pack(pady=5)

# =========================== Carga de Modelos =========================== #
# Cargar los modelos YOLO
modelos = {
    "activacion": YOLO("Modelos/Activacion.pt"),
    "acciones": YOLO("Modelos/Acciones.pt"),
    "lugar": YOLO("Modelos/Lugares.pt"),
    "tiempo": YOLO("Modelos/Tiempo.pt")
}

# ======================== Configuración de la Cámara ======================== #
# Crear pipeline para la cámara OAK-D
pipeline = dai.Pipeline()
cam_rgb = pipeline.create(dai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 480)
cam_rgb.setInterleaved(False)
cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
xout_video = pipeline.create(dai.node.XLinkOut)
xout_video.setStreamName("video")
cam_rgb.preview.link(xout_video.input)

# ===================== Variables de Control y Buffers ===================== #
model_actual = modelos["activacion"]
frase = ""
start_time = None
buffers = {
    "activacion": deque(maxlen=10),
    "acciones": deque(maxlen=15),
    "lugar": deque(maxlen=15),
    "tiempo": deque(maxlen=20)
}

# Datos de acciones, lugares y tiempos
acciones = ["Abrir", "Cerrar", "LuzOn", "LuzOff", "LuzOn", "LuzOff", "Segundo", "Minuto"]
lugares = ["Bano", "Casa", "Cocina", "Cocina", "Habitacion", "Sala"]
tiempos = ["1", "10", "2", "3", "4", "5"]

# ======================== Funciones de Detección ======================== #
# Función para procesar detección según el modelo actual
def procesar_detecciones(frame, model, buffer, clase_maxima):
    result = model.predict(frame, imgsz=640, conf=0.8)
    anotaciones = result[0].plot()

    for detection in result[0].boxes:
        class_id = int(detection.cls)
        confidence = float(detection.conf)
        if confidence >= 0.8:
            buffer.append(class_id)
            if len(buffer) == buffer.maxlen:
                return mode(buffer)
    return None

# Función para gestionar detecciones y cambiar de modelo
def gestionar_modelo(buffer, deteccion, modelo_siguiente, mensaje, accion=None):
    global model_actual, frase, start_time
    if deteccion is not None:
        if accion:
            frase += f" {accion}"
        model_actual = modelo_siguiente
        start_time = time.time()
        buffer.clear()

# ======================== Bucle Principal ======================== #
def iniciar_procesamiento():
    global model_actual, frase, start_time

    with dai.Device(pipeline) as device:
        video_queue = device.getOutputQueue(name="video", maxSize=8, blocking=False)
        topico = "CASA"
        mensaje = "Comunicacion Iniciada"

        while True:
            in_video = video_queue.get()
            frame = in_video.getCvFrame()

            if model_actual == modelos["activacion"]:
                deteccion = procesar_detecciones(frame, modelos["activacion"], buffers["activacion"], 0)
                if deteccion == 0:  # "Atencion" detectada
                    gestionar_modelo(buffers["activacion"], deteccion, modelos["acciones"], "Activación detectada", "Atencion")

            elif model_actual == modelos["acciones"]:
                deteccion = procesar_detecciones(frame, modelos["acciones"], buffers["acciones"], 7)
                if deteccion is not None and deteccion < len(acciones):
                    accion = acciones[deteccion]
                    modelo_siguiente = modelos["lugar"] if deteccion in [0, 1, 2, 3, 4, 5] else modelos["tiempo"]
                    gestionar_modelo(buffers["acciones"], deteccion, modelo_siguiente, accion, accion)

            elif model_actual == modelos["lugar"]:
                deteccion = procesar_detecciones(frame, modelos["lugar"], buffers["lugar"], 5)
                if deteccion is not None and deteccion < len(lugares):
                    lugar = "Cocina" if lugares[deteccion] == "Cocina" else lugares[deteccion]
                    frase += f" {lugar}"
                    topico = lugar
                    print(f"Frase final: {frase}")
                    publicar(topico, mensaje)
                    gestionar_modelo(buffers["lugar"], deteccion, modelos["activacion"], mensaje)

            elif model_actual == modelos["tiempo"]:
                deteccion = procesar_detecciones(frame, modelos["tiempo"], buffers["tiempo"], 5)
                if deteccion is not None and deteccion < len(tiempos):
                    tiempo = tiempos[deteccion]
                    frase += f" {tiempo}"
                    publicar("CASA", mensaje)
                    gestionar_modelo(buffers["tiempo"], deteccion, modelos["activacion"], mensaje)

            # Manejo de temporizadores para falsos positivos
            if start_time and time.time() - start_time > 10:
                print("Tiempo de espera excedido, reiniciando ciclo.")
                model_actual = modelos["activacion"]
                frase = ""

            # Actualizar interfaz gráfica
            actualizar_frase_final(frase, topico, mensaje)

            # Mostrar el fotograma anotado
            cv2.imshow("Video", frame)

            # Salir si se presiona 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Liberar recursos
    cv2.destroyAllWindows()
    client.loop_stop()
    client.disconnect()

# Iniciar la interfaz gráfica en un hilo separado para no bloquear el procesamiento
threading.Thread(target=iniciar_procesamiento, daemon=True).start()
root.mainloop()
