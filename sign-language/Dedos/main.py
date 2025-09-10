

# Importamos las librerías
from ultralytics import YOLO
import depthai as dai
import cv2

# Leer nuestro modelo
model = YOLO("C:/Users/enri-/Desktop/Tesis/Dedos/Acciones.pt")

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
        in_video = video_queue.get()
        frame = in_video.getCvFrame()
        
        # Leemos resultados
        result = model.predict(frame, imgsz=640, conf=0.5)
        
        # Extraer las anotaciones y clases detectadas
        anotaciones = result[0].plot()
        
        # Opcional: Procesar las detecciones
        for detection in result[0].boxes:
            class_id = int(detection.cls) # Obtener el ID de la clase
            confidence = detection.conf # Obtener la confianza de la detección
            box = detection.xyxy # Obtener las coordenadas de la caja delimitadora
        
        # Mostramos nuestro fotograma con anotaciones
        cv2.imshow("Deteccion y segmentacion", anotaciones)

        # Cerrar nuestro programa al presionar la tecla ESC
        if cv2.waitKey(1) == 27:
            break

    # Liberar recursos
    cv2.destroyAllWindows()
# 