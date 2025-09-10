import cv2
import glob
import xlsxwriter

workbook = xlsxwriter.Workbook('dataDientes_L.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 1
total_images_processed = 0  # Variable para contar el total de imágenes procesadas

#pathLetterImages = 'C:/Users/enri-/Desktop/10mo_Semestre/Vision_Artificial/Dientes_3/Grupos/'
pathLetterImages = 'C:/Users/enri-/Desktop/10mo_Semestre/Vision_Artificial/Dientes_3/Lados/Laterales/'

# vectorLetters = ['CAD','CAI','CD','CI','LD','LI']
# vectorLettersCount = [ 0, 0,0,0,0,0]

vectorLetters = ['LD','LI']
vectorLettersCount = [ 0, 0]

for indice, i in enumerate(vectorLetters):
    pathLett = pathLetterImages + i
    pathImages = glob.glob(pathLett + '/*.png')
    pathImages_limitado = pathImages[:50]
    for ruta in pathImages:
        imgColor = cv2.imread(ruta)
        imgGray = cv2.imread(ruta, 0)

        _, imgBinary = cv2.threshold(imgGray,0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        cnts, hier = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(cnts) > 0:
            vectorCaracter = []
            #c = max(contours, key = cv2.contourArea)
            # cv2.contourArea como encontrar el contorno mas grande
            for cnt in cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                areaWH = w * h
                area = cv2.contourArea(cnt)
                p = cv2.arcLength(cnt, True)
                imgRoi = imgBinary[y:y+h+10, x:x+w+10]
                imgRoiResize = cv2.resize(imgRoi, (40, 60))
                if areaWH > 1000:
                    #cv2.imshow('Imagen',imgRoiResize)
                    vectorCaracter = imgRoiResize.flatten()#.reshape(1, -1)
                    #vectorCaracter.append(area)
                    #vectorCaracter.append(p)
                    
                    for c in vectorCaracter:
                        worksheet.write(row, 0, indice)
                        worksheet.write(row, col, c)
                        col = col + 1
                    col = 1
                    row = row + 1
                    total_images_processed += 1  # Incrementar el contador de imágenes procesadas

            #print(f"Imagen procesada: {ruta}")
        #cv2.imshow('Imagen letra', imgBinary)
        
        cv2.waitKey(1)
cv2.destroyAllWindows()
workbook.close()

print(f"Total de imágenes procesadas: {total_images_processed}")

