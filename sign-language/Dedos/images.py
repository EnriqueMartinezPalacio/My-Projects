import depthai as dai
import cv2
import os
import uuid
import time
import threading

# Ruta de imágenes y configuración de etiquetas
images_path = 'C:/Users/enri-/Desktop/Tesis/Fotos'
labels = ['Atencion','LuzOn','LuzOff','Abrir','Cerrar','segundo','Minuto','Cocina','Casa','Sala','Habitacion','Bano','1','2','3','4','5','10']
number_img = 100

# Crear carpetas para las etiquetas
for label in labels:
    os.makedirs(os.path.join(images_path, label), exist_ok=True)

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

# Función para guardar imágenes en un hilo separado
def save_image(frame, label):
    image_name = os.path.join(images_path, label, label + '.' + '{}.jpg'.format(str(uuid.uuid1())))
    cv2.imwrite(image_name, frame)

# Conectar al dispositivo y empezar la captura
with dai.Device(pipeline) as device:
    video_queue = device.getOutputQueue(name="video", maxSize=8, blocking=False)
    
    for label in labels:
        print("Collecting images for {}".format(label))
        time.sleep(5)
        for img_num in range(number_img):
            in_video = video_queue.get()
            frame = in_video.getCvFrame()
            
            # Crear y lanzar un hilo para guardar la imagen
            threading.Thread(target=save_image, args=(frame, label)).start()
            cv2.imshow('frame', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cv2.destroyAllWindows()
