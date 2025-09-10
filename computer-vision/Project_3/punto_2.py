import numpy as np
import cv2
# Inicialización de variables globales
x1 = 0
y1 = 0
x2 = 0
y2 = 0
bandClick = False

# Función para obtener la ruta de la imagen
def getPath():
    path =  'images/monedas2.jpg'
    return path

# Función para cargar una imagen
def getImage(path, ch):
    image = cv2.imread(path, ch)
    return image
    
# Función para mostrar una imagen en una ventana
def showImg(nameW, img):
    cv2.imshow(nameW, img)

# Función para destruir todas las ventanas creadas por OpenCV
def destroy():
    cv2.destroyAllWindows()

# Función para obtener el tamaño de una imagen
def sizeImg(img):
    h,w = img.shape[:2]
    # print("h,w:",h,w)  # Comentario desactivado para no imprimir en cada iteración
    return h,w

# Función de callback para el evento del ratón
def mouseClick(event, x, y, flags, param):
    global x1, y1, x2, y2, bandClick
    if(event == cv2.EVENT_LBUTTONDOWN):        
        x1 = x
        y1 = y
        # print("x1 y y1",x1,y1)  # Comentario desactivado para no imprimir en cada clic
    elif(event == cv2.EVENT_LBUTTONUP):        
        x2 = x
        y2 = y
        # print("x2 y y2",x2,y2)  # Comentario desactivado para no imprimir en cada liberación de botón

        bandClick = True

# Función para obtener la región de interés (ROI) de una imagen
def getRoi(x1, y1, x2, y2, img):
    imgRoi = img[y1:y2, x1:x2]
    return imgRoi

# Función para binarizar una imagen
def binaryImg(imgGray):
    ret, imgBinary = cv2.threshold(imgGray, 199, 210, cv2.THRESH_BINARY_INV)
    return imgBinary

# Función principal
def main():
    global x1, y1, x2, y2, bandClick, monedas
    cv2.namedWindow("imgColor")
    cv2.namedWindow("imgGray")
    cv2.setMouseCallback("imgColor", mouseClick)
    imgColor = getImage(getPath(), 1)
    imgGray = getImage(getPath(), 0)
    y2, x2 = sizeImg(imgColor)

    while True:
        showImg("imgColor", imgColor)
        showImg("imgGray", imgGray)
        if bandClick:
            imgRoi = getRoi(x1, y1, x2, y2, imgColor)
            showImg("imgRoi", imgRoi)
            bandClick = False

        # Obtener umbral para binarizar imagen de forma semiautomática
        imgBinary = binaryImg(imgGray)
        showImg("imgBinary", imgBinary)

        # Contador de píxeles blancos
        pixeles_B = 0
        h, w = sizeImg(imgBinary)
        for i in range(h):
            for j in range(w):
                intensidad = imgBinary[i, j]
                if intensidad > 120:  # 255 es el valor para blanco en una imagen binarizada
                    pixeles_B += 1 # Me cuenta cuantos pixeles de un color mayor a 120 hay, esto debido a que si se iguala a 255 que es blanco no funcionaba 

        area_moneda = np.pi * (28 ** 2)
        # Se define el área de la moneda promedio mediante el uso de ROI, donde el área se obtiene posicionando el cursor en la mitad
        # de la moneda y arrastrándolo en línea recta hacia el lado de la moneda, después, con las coordenadas x1 y x2 se obtiene el radio y, con eso, el área
        monedas = int(pixeles_B / area_moneda)
        # Se utiliza int para que me entregue un valor entero, la fórmula utilizada consiste en dividir la 
        # sumatoria de píxeles blancos o semejantes entre el área de la moneda promedio
        print("Numero de monedas:", monedas)  # Imprimir el número de monedas adentro del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # print("Numero de monedas:", monedas)  # Imprimir el número de monedas fuera del bucle
    destroy()

if __name__ == "__main__":
   main()