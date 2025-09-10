# Importamos las librerías necesarias
from ultralytics import YOLO
import depthai as dai
import cv2
import torch

# Cargamos el modelo
model = YOLO("Tiempo.pt")  # Reemplaza "Modelo.pt" con el nombre de tu modelo

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

# Conectar al dispositivo y empezar la captura
with dai.Device(pipeline) as device:
    video_queue = device.getOutputQueue(name="video", maxSize=8, blocking=False)

    while True:
        # Tomar fotograma de la cámara
        in_video = video_queue.get()
        frame = in_video.getCvFrame()

        # Realizar predicción con el modelo
        result = model.predict(frame, imgsz=640, conf=0.5)

        # Extraer anotaciones y clases detectadas
        anotaciones = result[0].plot()

        # Procesar las detecciones
        detected_indices = []
        for detection in result[0].boxes:
            class_id = int(detection.cls)  # Obtener el ID de la clase
            confidence = float(detection.conf)  # Convertir la confianza a flotante

            # Imprimir información de detección en la consola
            print(f"Detectado: ID={class_id}, Confianza={confidence:.2f}, Coordenadas={detection.xyxy}")

            if confidence >= 0.5:
                detected_indices.append((class_id, confidence))

        # Mostrar los índices detectados y sus confidencias en la imagen
        if detected_indices:
            text = "Índices detectados:\n" + "\n".join(f"ID: {idx}, Conf: {conf:.2f}" for idx, conf in detected_indices)
            cv2.putText(anotaciones, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

        # Mostrar el fotograma con anotaciones
        cv2.imshow("Detección y Segmentación", anotaciones)

        # Cerrar el programa al presionar la tecla ESC
        if cv2.waitKey(1) == 27:
            break

    # Liberar recursos
    cv2.destroyAllWindows()
