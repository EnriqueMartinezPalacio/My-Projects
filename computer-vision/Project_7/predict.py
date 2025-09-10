import glob
import joblib

# Carga los modelos


model_letras = joblib.load('modelMLPLetras.joblib')
model_numeros = joblib.load('modelMLPNumeros.joblib')
escaler_letras = joblib.load('modelScalerLetras.joblib')
escaler_numeros = joblib.load('modelScalerNumeros.joblib')

 
 
import numpy as np
import cv2
import glob



# Definir mapeos para las letras y números según lo que tu modelo predice
char_map_letras = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}
char_map_numeros = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}

def testimg(imgRoi, val):
    # Preparar la imagen para el modelo
    imgRoi_resized = cv2.resize(imgRoi, (40, 60))  # Asume que el modelo espera imágenes de 20x20
    imgRoi_flattened = imgRoi_resized.flatten().reshape(1, -1)  # Aplanar la imagen

    # Decidir qué modelo y escalador usar
    if val == 1:  # Letras
        imgRoi_scaled = escaler_letras.transform(imgRoi_flattened)
        prediction = model_letras.predict(imgRoi_scaled)
        result = char_map_letras[int(prediction[0])]  # Usar el mapeo para convertir el número en letra
    else:  # Números
        imgRoi_scaled = escaler_numeros.transform(imgRoi_flattened)
        prediction = model_numeros.predict(imgRoi_scaled)
        result = char_map_numeros[int(prediction[0])]  # Usar el mapeo para convertir el número en número

    return result  # Devolver el carácter interpretado

 
 
filepaths=['test/placas_1','test/placas_2']
print("Presiona Q para cancelar")
for fold in filepaths:
    pathImages= glob.glob(fold + '/*.jpg')
    for pathimg in pathImages:
        placa=[]
        imgColor=cv2.imread(pathimg)
        # imgcolor=cv2.resize(imgColor,(420,210))
        imgGray=cv2.cvtColor(imgColor,cv2.COLOR_BGR2GRAY)
        ret,imgBin=cv2.threshold(imgGray,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        # kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2)) #kernel erosion
        # imgfilt=cv2.erode(imgBin,kernel=kernel,iterations=1)
        cv2.imshow('Binarized',cv2.resize(imgBin,(420,210)))
        # cv2.imshow('erosion',cv2.resize(imgfilt,(420,210)))
        # imgBin=imgfilt
        cnts,hier=cv2.findContours(imgBin,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)#hallo el contorno externo
        if (len(cnts)>0):#si encuentro al menos un contorno
            lastcenter=0
            for idx,cnt in enumerate(cnts): #recorro todos los contornos
                x,y,w,h=cv2.boundingRect(cnt)
                ratio=h/w
                centery=y+(h/2)
                rect=[x,y,w,h]
                if(cv2.contourArea(cnt)>30) and ratio<5 and ratio>1 and cv2.contourArea(cnt)<1100 and abs(centery-35)<4 and abs(x+(w/2) - lastcenter)>1:
                    # print(abs(x+(w/2) - lastcenter))
                    if(x+(w/2)<70):
                        val=1
                    else:
                        val=0
                    cv2.rectangle(imgColor,(x,y),(x+w,y+h),(255,0,0),1)
                    cv2.line(imgColor,(70,1),(70,70),(255,0,0))
                    imgRoi=imgBin[y:y+h,x:x+w]
                    cv2.imshow('ROI',imgRoi)
                    cv2.waitKey(1)
                    
                    placa.append(testimg(imgRoi,val))
                lastcenter=x+(w/2)
        cv2.imshow('Current image',cv2.resize(imgColor,(420,210)))
        # print(placa)
        placa.reverse()
        for string in placa:
            print(string,end="")
        print('')
        if(cv2.waitKey(0) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break
    else:
        continue
    break