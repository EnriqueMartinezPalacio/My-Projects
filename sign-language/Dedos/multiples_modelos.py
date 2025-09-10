# Importamos las librerías necesarias
from ultralytics import YOLO
import depthai as dai
import cv2

# Cargamos los modelos
model_activacion = YOLO("Activacion.pt")
model_acciones = YOLO("Acciones_Este.pt")
model_lugar = YOLO("Lugares.pt")
model_tiempo = YOLO("Tiempo.pt")

# Crear pipeline para la cámara OAK-D
pipeline = dai.Pipeline()

# Definir nodo de la cámara de color
cam_rgb = pipeline.create(dai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 480)
cam_rgb.setInterleaved(False)
cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)

# Nodo para la salida de video
xout_video = pipeline.create(dai.node.XLinkOut)
xout_video.setStreamName("video")

# Vincular la cámara a la salida de video
cam_rgb.preview.link(xout_video.input)

# Variables para controlar el flujo
current_model = model_activacion

# Conectar al dispositivo y empezar la captura
with dai.Device(pipeline) as device:
    video_queue = device.getOutputQueue(name="video", maxSize=8, blocking=False)

    while True:
        # Tomar fotograma de la cámara
        in_video = video_queue.get()
        frame = in_video.getCvFrame()

        # Realizar predicción con el modelo actual
        result = current_model.predict(frame, imgsz=640, conf=0.5)

        # Extraer anotaciones y clases detectadas
        anotaciones = result[0].plot()

        # Procesar las detecciones
        for detection in result[0].boxes:
            class_id = int(detection.cls)  # Obtener el ID de la clase
            confidence = detection.conf  # Obtener la confianza de la detección
            box = detection.xyxy  # Obtener las coordenadas de la caja delimitadora

            # Cambiar el modelo dependiendo de la clase detectada
            if current_model == model_activacion:
                if class_id == 0:  # Seña de "Atencion"
                    current_model = model_acciones
                    print("Se activó el modelo de Acciones.")
            elif current_model == model_acciones:
                if class_id in [0, 1,2,3]:  # Señas de "Minuto" o "Segundo"
                    current_model = model_lugar
                    print("Se activó el modelo de Tiempo.")
                elif class_id in [4,5]:  # Otras acciones (Abrir, Cerrar, On, Off)
                    current_model = model_tiempo
                    print("Se activó el modelo de Lugar.")
            elif current_model == model_lugar:
                # Aquí podrías agregar lógica adicional si es necesario
                pass
            elif current_model == model_tiempo:
                # Aquí podrías agregar lógica adicional si es necesario
                pass

        # Mostrar el fotograma con anotaciones
        cv2.imshow("Deteccion y segmentacion", anotaciones)

        # Cerrar el programa al presionar la tecla ESC
        if cv2.waitKey(1) == 27:
            break

    # Liberar recursos
    cv2.destroyAllWindows()

