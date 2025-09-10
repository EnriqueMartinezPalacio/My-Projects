# import cv2

# # Abrir el video
# video_path = 'videos/video_caninoDer.avi'
# cap = cv2.VideoCapture(video_path)

# # Variables para contar los dientes detectados
# total_dientes_detectados = 0

# while cap.isOpened():
#     ret, frame = cap.read()

#     if not ret:
#         break

#     # Convertir el frame a escala de grises
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Binarizar el frame
#     _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

#     # Encontrar contornos en la imagen binarizada
#     contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#     # Iterar sobre los contornos encontrados
#     for contour in contours:
#         # Calcular el área del contorno
#         area = cv2.contourArea(contour)

#         # Si el área del contorno es lo suficientemente grande como para ser considerado un diente
#         if area > 1000:
#             total_dientes_detectados += 1

#             # Dibujar un rectángulo alrededor del diente detectado en el frame original
#             x, y, w, h = cv2.boundingRect(contour)
#             cv2.rectangle(binary, (x-15, y-15), (x + w+15, y + h+15), (255, 0, 0), 2)

#             # Extraer la región de interés (ROI) donde se encuentra el diente
#             roi = frame[y-15:y + h+15, x-15:x + w+15]

#             # Guardar la imagen ROI en un archivo
#             roi_filename = f'images/CAD/CAD_{total_dientes_detectados}.png'
#             cv2.imwrite(roi_filename, roi)

#     # Mostrar el frame con los dientes detectados
#     cv2.imshow('Detección de dientes', frame)

#     # Esperar 1 milisegundo y salir del bucle si se presiona 'q'
#     if cv2.waitKey(60) & 0xFF == ord('q'):
#         break

# # Liberar los recursos
# cap.release()
# cv2.destroyAllWindows()

# print(f'Se detectaron y guardaron {total_dientes_detectados} dientes.')



import cv2

# Abrir el video
video_path = 'videos/video_laterIzq.avi'
cap = cv2.VideoCapture(video_path)

# Variables para contar los dientes detectados
total_dientes_detectados = 0

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Binarizar el frame
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    # Encontrar contornos en la imagen binarizada
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Iterar sobre los contornos encontrados
    for contour in contours:
        # Calcular el área del contorno
        area = cv2.contourArea(contour)

        # Si el área del contorno es lo suficientemente grande como para ser considerado un diente
        if area > 1000:
            total_dientes_detectados += 1

            # Dibujar un rectángulo alrededor del diente detectado en el frame original
            x, y, w, h = cv2.boundingRect(contour)
            #cv2.rectangle(frame, (x-15, y-15), (x + w+15, y + h+15), (255, 0, 0), 2)

            # Definir un factor de escala para aumentar el tamaño de la ROI
            scale_factor = 1.5

            # Ajustar los límites de la región de interés (ROI) para hacerla más grande
            roi = frame[int(max(0, y - 15 * scale_factor)):int(min(frame.shape[0], y + h + 15 * scale_factor)),
                        int(max(0, x - 15 * scale_factor)):int(min(frame.shape[1], x + w + 15 * scale_factor))]

            # Guardar la imagen ROI en un archivo
            roi_filename = f'images/LI/LI_{total_dientes_detectados}.png'
            cv2.imwrite(roi_filename, roi)

    # Mostrar el frame con los dientes detectados
    cv2.imshow('Detección de dientes', frame)

    # Esperar 1 milisegundo y salir del bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()

print(f'Se detectaron y guardaron {total_dientes_detectados} dientes.')
