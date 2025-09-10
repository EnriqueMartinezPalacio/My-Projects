import cv2
import numpy as np
import joblib
import os

# Carga de los modelos
mlp = joblib.load('modelMLP_Todo.joblib')
skl = joblib.load('modelScaler_Todo.joblib')

print("Modelo cargado...", mlp)
#Limon_>PaPA
#Cebolla->Tomate
#
folder_path = 'C:/Users/enri-/Desktop/10mo_Semestre/Vision_Artificial/Final/ROI/Tomate'

for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(folder_path, filename)
        frame = cv2.imread(image_path)

        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, imgBinary = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cnts, _ = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Variable para indicar si se ha detectado una fruta
        fruta_detectada_flag = False

        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            areaWH = w * h
            if areaWH > 1000:
                if not fruta_detectada_flag:  # Solo procesar si no se ha detectado ninguna fruta
                    imgRoi = imgBinary[y:y+h+10, x:x+w+10]
                    imgRoiResize = cv2.resize(imgRoi, (40, 60))

                    vectorCaracter = imgRoiResize.flatten()
                    vectorReshape = vectorCaracter.reshape(1, -1)
                    vectorSKL = skl.transform(vectorReshape)

                    result = mlp.predict(vectorSKL)
                    if result == 0:
                        print("Fruta: Cebolla")
                        text = "Fruta: Cebolla"
                        calidad = "Buena" if mlp.predict_proba(vectorSKL)[0][1] > 0.5 else "Mala"
                        print("Calidad:", calidad)
                    elif result == 1:
                        print("Fruta: Tomate")
                        text = "Fruta: Tomate"
                        calidad = "Buena" if mlp.predict_proba(vectorSKL)[0][1] > 0.5 else "Mala"
                        print("Calidad:", calidad)
                    elif result == 2:
                        print("Fruta: Limon")
                        text = "Fruta: Limon"
                        calidad = "Buena" if mlp.predict_proba(vectorSKL)[0][1] > 0.5 else "Mala"
                        print("Calidad:", calidad)
                    elif result == 3:
                        print("Fruta: Papa")
                        text = "Fruta: Papa"
                        calidad = "Buena" if mlp.predict_proba(vectorSKL)[0][1] > 0.5 else "Mala"
                        print("Calidad:", calidad)

                    # Dibuja el cuadro delimitador
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Dibuja el texto sobre la imagen
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(frame, calidad, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Marcar que se ha detectado una fruta
                    fruta_detectada_flag = True

        # Mostrar el fotograma
        cv2.imshow("Frame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
