# import cv2
# import numpy as np
# import joblib

# # Carga de los modelos
# mlp = joblib.load('modelMLP.joblib')
# skl = joblib.load('modelScaler.joblib')
# mlp_Centrales = joblib.load('modelMLP_C.joblib')
# skl_Centrales = joblib.load('modelScaler_C.joblib')
# mlp_Caninos = joblib.load('modelMLP_CA.joblib')
# skl_Caninos = joblib.load('modelScaler_CA.joblib')
# mlp_Lateral = joblib.load('modelMLP_L.joblib')
# skl_Lateral = joblib.load('modelScaler_L.joblib')

# print("Modelo cargado...", mlp)

# video_path = 'videos/video_laterIzq.avi'
# cap = cv2.VideoCapture(video_path)

# # Dimensiones de la ventana
# window_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# window_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# # Coordenadas de la región de interés (ROI) de la bandera
# flag_roi_x = int(window_width / 3)
# flag_roi_y = int(window_height / 3)
# flag_roi_w = int(window_width / 3)
# flag_roi_h = int(window_height / 3)

# # Variable para indicar si se ha detectado un diente en la bandera
# diente_detectado_flag = False

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     _, imgBinary = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#     cnts, _ = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#     for cnt in cnts:
#         x, y, w, h = cv2.boundingRect(cnt)
#         areaWH = w * h
#         if areaWH > 1000:
#             # Verificar si el diente está dentro de la región de interés de la bandera
#             if x < flag_roi_x + flag_roi_w and x + w > flag_roi_x and y < flag_roi_y + flag_roi_h and y + h > flag_roi_y:
#                 if not diente_detectado_flag:  # Solo procesar si no se ha detectado ningún diente en la bandera
#                     imgRoi = imgBinary[y:y+h+10, x:x+w+10]
#                     imgRoiResize = cv2.resize(imgRoi, (40, 60))

#                     vectorCaracter = imgRoiResize.flatten()
#                     vectorReshape = vectorCaracter.reshape(1, -1)
#                     vectorSKL = skl.transform(vectorReshape)

#                     result = mlp.predict(vectorSKL)
#                     # if result == 0:
#                     #     print("Canino")
#                     # elif result == 1:
#                     #     print("Central")
#                     # elif result == 2:
#                     #     print("Lateral")
#                     if result == 0:
#                         #print("Canino")
#                         result_Canino = mlp_Caninos.predict(skl_Caninos.transform(vectorReshape))
#                         if result_Canino == 1:
#                             print("Diente: Canino Izquierdo")
#                         elif result_Canino == 0:
#                             print("Diente: Canino Derecho")
#                     elif result == 1:
#                         #print("Central")
#                         result_Centrales = mlp_Centrales.predict(skl_Centrales.transform(vectorReshape))
#                         if result_Centrales == 1:
#                             print("Diente: Central Izquierdo")
#                         elif result_Centrales == 0:
#                             print("Diente: Central Derecho")
#                     elif result == 2:
#                         #print("Lateral")
#                         result_Lateral = mlp_Lateral.predict(skl_Lateral.transform(vectorReshape))
#                         if result_Lateral == 1:
#                             print("Diente: Lateral Izquierdo")
#                         elif result_Lateral == 0:
#                             print("Diente: Lateral Derecho")

#                     # Dibuja el cuadro delimitador
#                     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#                     # Marcar que se ha detectado un diente en la bandera
#                     diente_detectado_flag = True

#     # Mostrar el fotograma
#     cv2.imshow("Frame", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     # Reiniciar la bandera de detección de dientes cuando la bandera no esté en la región de interés
#     if flag_roi_x > x + w or flag_roi_x + flag_roi_w < x or flag_roi_y > y + h or flag_roi_y + flag_roi_h < y:
#         diente_detectado_flag = False

# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
import joblib

# Carga de los modelos
mlp = joblib.load('modelMLP.joblib')
skl = joblib.load('modelScaler.joblib')
mlp_Centrales = joblib.load('modelMLP_C.joblib')
skl_Centrales = joblib.load('modelScaler_C.joblib')
mlp_Caninos = joblib.load('modelMLP_CA.joblib')
skl_Caninos = joblib.load('modelScaler_CA.joblib')
mlp_Lateral = joblib.load('modelMLP_L.joblib')
skl_Lateral = joblib.load('modelScaler_L.joblib')

print("Modelo cargado...", mlp)

video_path = 'videos/video_caninoIzq.avi'
cap = cv2.VideoCapture(video_path)

# Dimensiones de la ventana
window_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
window_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Coordenadas de la región de interés (ROI) de la bandera
flag_roi_x = int(window_width / 3)
flag_roi_y = int(window_height / 3)
flag_roi_w = int(window_width / 3)
flag_roi_h = int(window_height / 3)

# Variable para indicar si se ha detectado un diente en la bandera
diente_detectado_flag = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, imgBinary = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cnts, _ = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        areaWH = w * h
        if areaWH > 1000:
            # Verificar si el diente está dentro de la región de interés de la bandera
            if x < flag_roi_x + flag_roi_w and x + w > flag_roi_x and y < flag_roi_y + flag_roi_h and y + h > flag_roi_y:
                if not diente_detectado_flag:  # Solo procesar si no se ha detectado ningún diente en la bandera
                    imgRoi = imgBinary[y:y+h+10, x:x+w+10]
                    imgRoiResize = cv2.resize(imgRoi, (40, 60))

                    vectorCaracter = imgRoiResize.flatten()
                    vectorReshape = vectorCaracter.reshape(1, -1)
                    vectorSKL = skl.transform(vectorReshape)

                    result = mlp.predict(vectorSKL)
                    # if result == 0:
                    #     print("Canino")
                    # elif result == 1:
                    #     print("Central")
                    # elif result == 2:
                    #     print("Lateral")
                    if result == 0:
                        #print("Canino")
                        result_Canino = mlp_Caninos.predict(skl_Caninos.transform(vectorReshape))
                        if result_Canino == 1:
                            print("Diente: Canino Izquierdo")
                            text = "Diente: Canino Izquierdo"
                        elif result_Canino == 0:
                            print("Diente: Canino Derecho")
                            text = "Diente: Canino Derecho"
                    elif result == 1:
                        #print("Central")
                        result_Centrales = mlp_Centrales.predict(skl_Centrales.transform(vectorReshape))
                        if result_Centrales == 1:
                            print("Diente: Central Izquierdo")
                            text = "Diente: Central Izquierdo"
                        elif result_Centrales == 0:
                            print("Diente: Central Derecho")
                            text = "Diente: Central Derecho"
                    elif result == 2:
                        #print("Lateral")
                        result_Lateral = mlp_Lateral.predict(skl_Lateral.transform(vectorReshape))
                        if result_Lateral == 1:
                            print("Diente: Lateral Izquierdo")
                            text = "Diente: Lateral Izquierdo"
                        elif result_Lateral == 0:
                            print("Diente: Lateral Derecho")
                            text = "Diente: Lateral Derecho"

                    # Dibuja el cuadro delimitador
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Dibuja el texto sobre la imagen
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Marcar que se ha detectado un diente en la bandera
                    diente_detectado_flag = True

    # Mostrar el fotograma
    cv2.imshow("Frame", frame)
    
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    # Reiniciar la bandera de detección de dientes cuando la bandera no esté en la región de interés
    if flag_roi_x > x + w or flag_roi_x + flag_roi_w < x or flag_roi_y > y + h or flag_roi_y + flag_roi_h < y:
        diente_detectado_flag = False

cap.release()
cv2.destroyAllWindows()
