# Importamos las librerías necesarias
from ultralytics import YOLO
import depthai as dai
import cv2
import time
from collections import deque
from statistics import mode
import tkinter as tk
import paho.mqtt.client as mqtt
import threading 
import queue
# =========================== MQTT Configuración =========================== #
# Configuración del broker MQTT
broker = "broker.emqx.io"
puerto = 8883

# Función de conexión al broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
    else:
        print(f"Conexión fallida, código de error {rc}")

# Crear una instancia del cliente MQTT
client = mqtt.Client()

# Configuración TLS y conexión al broker
client.tls_set()
client.on_connect = on_connect
client.connect(broker, puerto)

# Función para publicar un mensaje a un tópico
def publicar(topico, mensaje):
    client.publish(topico, mensaje)
    print(f"Mensaje '{mensaje}' enviado al tópico '{topico}'")

# Iniciar el loop de procesamiento MQTT
client.loop_start()

# ======================== Interfaz gráfica (Tkinter) ======================== #
# Función para actualizar la ventana con la frase final
def actualizar_frase_final(frase, topico, mensaje,tiempo_formateado):
    frase_label.config(text=f"Frase Final: {frase}")
    topico_label.config(text=f"Tópico: {topico}")
    mensaje_label.config(text=f"Mensaje: {mensaje}")
    tiempo_label.config(text=f"Tiempo:{tiempo_formateado}")
    root.update_idletasks()

# Inicializar la ventana de tkinter
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
tiempo_label = tk.Label(root, text="Tiempo: ", font=("Arial", 12))
tiempo_label.pack(pady=5)
# =========================== Carga de Modelos =========================== #
# Cargamos los modelos de YOLO
model_activacion = YOLO("Activacion.pt")
model_acciones = YOLO("Acciones_2.pt")
model_lugar = YOLO("Lugares.pt")
model_tiempo = YOLO("Tiempo.pt")

# ======================== Configuración de la Cámara ======================== #
# Crear pipeline para la cámara OAK-D
pipeline = dai.Pipeline()

# Definir nodo de la cámara de color
cam_rgb = pipeline.create(dai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 480)
cam_rgb.setInterleaved(False)
cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)

# Nodo para la salida de video
xout_video = pipeline.create(dai.node.XLinkOut)
xout_video.setStreamName("video")

# Vincular la cámara a la salida de video
cam_rgb.preview.link(xout_video.input)

# ===================== Variables de Control y Buffers ===================== #
current_model = model_activacion  # Modelo actual
frase = ""  # Frase acumulada

# Buffers para detección
detection_buffer_activacion = deque(maxlen=5)  # Buffer para activación
detection_buffer_acciones = deque(maxlen=20)    # Buffer para acciones
detection_buffer_lugar = deque(maxlen=35)       # Buffer para lugares
detection_buffer_tiempo = deque(maxlen=15)      # Buffer para tiempo

# Variables de tiempo
start_time = None
timeout_activacion = 10  # Tiempo de espera en segundos
timeout_acciones = 10
timeout_lugar = 10
timeout_tiempo = 10

#Variables temprizador
tiempo_formateado = "00:00"  # Definición por defecto
temporizador_activo = False  # Inicialización de la variable global
temporizador_thread=None #Hilo del temporizador

# Listas de índices para acciones, lugares y tiempos
acciones = ["Abrir", "Cerrar", "LuzOn", "LuzOff", "LuzOn", "LuzOff", "Segundo", "Minuto"]
lugares = ["Bano", "Casa", "Cocina", "Cocina", "Habitacion", "Sala"]
tiempos = ["1", "10", "2", "3", "4", "5"]

# Inicializar las variables del tópico y mensaje
topico = "CASA"
mensaje = "Comunicacion Iniciada"

# ======================== Funcion del temporizador ======================== #
# Cola para manejar la comunicación entre hilos
tiempo_queue = queue.Queue()
def detener_temporizador():
    """Funcion para detner el temporizador activo"""
    global temporizador_activo
    if temporizador_activo:
        temporizador_activo=False

def temporizador(duracion, unidad):
    global temporizador_activo

    # Convertir duración a segundos si está en minutos
    if unidad == "Minuto":
        duracion = duracion * 60

    tiempo_restante = duracion
    while tiempo_restante > 0 and temporizador_activo:
        minutos = tiempo_restante // 60  # Calcula los minutos
        segundos = tiempo_restante % 60  # Calcula los segundos restantes
        tiempo_formateado = f"{minutos:02d}:{segundos:02d}"  # Formato MM:SS

        # Enviar tiempo formateado a la cola
        tiempo_queue.put(tiempo_formateado)

        # Esperar 1 segundo antes de disminuir el tiempo
        time.sleep(1)
        tiempo_restante -= 1
    if tiempo_restante <= 0 and temporizador_activo:
        # Cuando llega a 00:00, enviar al tópico MQTT
        tiempo_queue.put("00:00")
        publicar("Casa", "Tiempo")
    temporizador_activo = False  # Resetear bandera de temporizador

def iniciar_temporizador(duracion, unidad):
    global temporizador_activo,temporizador_thread

    """Si hay un temporizador activo,se detiene antes de iniciar uno nuevo"""
    if temporizador_activo:
        detener_temporizador()
        if temporizador_thread is not None:
            temporizador_thread.join() #Espera  a que el hilo del temporizador termine
    
    temporizador_activo=True
    temporizador_thread=threading.Thread(target=temporizador,args=(duracion,unidad))
    temporizador_thread.start()
    

# ======================== Lógica de Detección y Control ======================== #
# Conectar al dispositivo y empezar la captura de video
with dai.Device(pipeline) as device:
    video_queue = device.getOutputQueue(name="video", maxSize=8, blocking=False)

    while True:
        # Obtener fotograma de la cámara
        in_video = video_queue.get()
        frame = in_video.getCvFrame()

        # Realizar predicción con el modelo actual
        result = current_model.predict(frame, imgsz=640, conf=0.8)

        # Extraer anotaciones y clases detectadas
        anotaciones = result[0].plot()

        # Procesar las detecciones
        for detection in result[0].boxes:
            class_id = int(detection.cls)  # Obtener el ID de la clase
            confidence = float(detection.conf)  # Obtener confianza

            if confidence >= 0.8:
                if current_model == model_activacion:
                    detection_buffer_activacion.append(class_id)
                elif current_model == model_acciones:
                    detection_buffer_acciones.append(class_id)
                elif current_model == model_lugar:
                    detection_buffer_lugar.append(class_id)
                elif current_model == model_tiempo:
                    detection_buffer_tiempo.append(class_id)

        # Procesar el buffer de activación
        if len(detection_buffer_activacion) == detection_buffer_activacion.maxlen:
            try:
                most_common_detection = mode(detection_buffer_activacion)
                if most_common_detection == 0:  # Seña de "Atencion"
                    current_model = model_acciones
                    publicar("Casa", "Sena")
                    frase = "Atencion"
                    mensaje = "Activación detectada"
                    print("Se activó el modelo de Acciones.")
                    detection_buffer_activacion.clear()
                    start_time = time.time()

            except Exception as e:
                print(f"Error en el procesamiento de activación: {e}")
        # Procesar el buffer de acciones
        if len(detection_buffer_acciones) == detection_buffer_acciones.maxlen:
            try:
                most_common_detection = mode(detection_buffer_acciones)
                if 0 <= most_common_detection < len(acciones):
                    if most_common_detection in [0, 1]:  # "Abrir" o "Cerrar"
                        current_model = model_lugar
                        publicar("Casa", "Sena")
                        frase += f" {acciones[most_common_detection]}"
                        mensaje = acciones[most_common_detection]  # Actualizar mensaje correctamente
                    elif most_common_detection in [2, 3]:  # "LuzOn" o "LuzOff"
                        current_model = model_lugar
                        frase += " LuzOff"  # Agregar LuzOn a la frase
                        mensaje = "LuzOff"  # Asegurarse de que el mensaje también sea LuzOn
                    elif most_common_detection in [4, 5]:  # "LuzOn" o "LuzOff"
                        current_model = model_lugar
                        frase += " LuzOn"  # Agregar LuzOff a la frase
                        mensaje = "LuzOn"  # Asegurarse de que el mensaje también sea LuzOff
                    elif most_common_detection in [6, 7]:  # "Minuto" o "Segundo"
                        current_model = model_tiempo
                        frase += " Minuto" if most_common_detection == 6 else " Segundo"
                        mensaje = "Minuto" if most_common_detection == 6 else "Segundo"
                    start_time = time.time()
                detection_buffer_acciones.clear()

            except Exception as e:
                print(f"Error en el procesamiento de acciones: {e}")

        # Procesar el buffer de lugares
        if len(detection_buffer_lugar) == detection_buffer_lugar.maxlen:
            try:
                most_common_detection = mode(detection_buffer_lugar)
                if 0 <= most_common_detection < len(lugares):
                    publicar("Casa", "Sena")
                    topico = lugares[most_common_detection]
                    lugar = "Cocina" if topico == "Cocina" else topico
                    frase += f" {lugar}"
                    print(f"Frase final: {frase}")
                    publicar(topico, mensaje)
                    current_model = model_activacion
                    start_time = time.time()
                detection_buffer_lugar.clear()

            except Exception as e:
                print(f"Error en el procesamiento de lugares: {e}")

        if len(detection_buffer_tiempo) == detection_buffer_tiempo.maxlen:
            try:
                most_common_detection = mode(detection_buffer_tiempo)
                if 0 <= most_common_detection < len(tiempos):
                    publicar("Casa", "Sena")
                    tiempo_total = int(tiempos[most_common_detection])  # Convertir a entero
                    frase += f" {tiempo_total}"
                    
                    # Detectar si es minuto o segundo
                     # Detectar si la última acción fue "Minuto" o "Segundo"
                    if "Minuto" in mensaje:
                        iniciar_temporizador(tiempo_total, "Minuto")  # Iniciar temporizador para minutos
                    elif "Segundo" in mensaje:
                        iniciar_temporizador(tiempo_total, "Segundo")  # Iniciar temporizador para segundos

                
                    detection_buffer_tiempo.clear()
                    current_model = model_activacion

            except Exception as e:
                print(f"Error en el procesamiento de tiempo: {e}")

        # Verificar si hay una actualización de tiempo en la cola
        if not tiempo_queue.empty():
            tiempo_formateado = tiempo_queue.get()  # Obtener tiempo actualizado
            actualizar_frase_final(frase, topico, mensaje, tiempo_formateado)  # Actualizar la interfaz

        # Manejar falsos positivos con temporizadores
        if start_time:
            elapsed_time = time.time() - start_time
            if current_model == model_acciones and elapsed_time > timeout_acciones:
                print("Tiempo de espera excedido en acciones, reiniciando ciclo.")
                publicar("Casa","Reinicio")
                current_model = model_activacion
                frase = ""
            elif current_model == model_lugar and elapsed_time > timeout_lugar:
                print("Tiempo de espera excedido en lugares, reiniciando ciclo.")
                publicar("Casa","Reinicio")
                current_model = model_activacion
                frase = ""
            elif current_model == model_tiempo and elapsed_time > timeout_tiempo:
                print("Tiempo de espera excedido en tiempo, reiniciando ciclo.")
                publicar("Casa","Reinicio")
                current_model = model_activacion
                frase = ""

        # Actualizar la ventana de tkinter
        actualizar_frase_final(frase, topico, mensaje,tiempo_formateado)

        # Mostrar el fotograma anotado
        cv2.imshow("Video", anotaciones)

        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberar recursos
cv2.destroyAllWindows()
client.loop_stop()
client.disconnect()
