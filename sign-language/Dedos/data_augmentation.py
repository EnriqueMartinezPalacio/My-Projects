import cv2
import numpy as np
import os
import random

def rotate_image(image, angle):
    """
    Rota la imagen por un ángulo dado.
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    """
    Ajusta el brillo y contraste de la imagen.
    """
    beta = brightness  # Brillo
    alpha = 1 + (contrast / 100.0)  # Contraste
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

def resize_with_padding(image, target_size):
    """
    Redimensiona la imagen manteniendo la relación de aspecto y agrega bordes para ajustar al tamaño objetivo.
    """
    old_size = image.shape[:2]
    ratio = min(target_size[0] / old_size[0], target_size[1] / old_size[1])
    new_size = (int(old_size[1] * ratio), int(old_size[0] * ratio))
    resized = cv2.resize(image, new_size)

    delta_w = target_size[1] - new_size[0]
    delta_h = target_size[0] - new_size[1]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    color = [0, 0, 0]  # Negro
    new_image = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return new_image

def data_augmentation(input_folder, output_folder, target_size=(640, 640), num_augmentations=5):
    """
    Aplica augmentaciones a las imágenes de una carpeta de entrada y las guarda en la carpeta de salida.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            for i in range(num_augmentations):
                # Rotación entre -15 y 15 grados
                angle = random.uniform(-15, 15)
                rotated = rotate_image(image, angle)

                # Ajuste de brillo y contraste
                brightness = random.randint(-30, 30)  # Aleatorio entre -30 y 30
                contrast = random.randint(-30, 30)   # Aleatorio entre -30 y 30
                bright_contrast = adjust_brightness_contrast(rotated, brightness, contrast)

                # Redimensionar con padding
                resized = resize_with_padding(bright_contrast, target_size)

                # Guardar la imagen aumentada
                output_filename = f"{os.path.splitext(filename)[0]}_aug_{i}.jpg"
                output_path = os.path.join(output_folder, output_filename)
                cv2.imwrite(output_path, resized)

    print(f"Data augmentation completada. Imágenes guardadas en: {output_folder}")

# Configuración
input_folder = "C:/Users/enri-/Desktop/Tesis/DATA/Fotos/Acciones/Abrir/"  # Reemplazar con la ruta a tu carpeta de imágenes
output_folder = "C:/Users/enri-/Desktop/Tesis/DATA/Fotos/Acciones/Abrir_Aug/"  # Reemplazar con la ruta donde guardarás las imágenes aumentadas

# Ejecutar el script
data_augmentation(input_folder, output_folder)
