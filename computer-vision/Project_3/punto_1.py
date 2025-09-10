# Se importan las bibliotecas necesarias: 
import cv2  #cv2 para OpenCV
import numpy as np  #numpy para operacion matematicas
import random # random para generar numeros aleatorios

# Se inicializan las variables, para las coordenadas del clic del raton
x1=0
y1=0
x2=0
y2=0
bandClick= False #Se inicializa bandClick para indicar que se ha hecho click

# Se define la funcion getPath, para devoler la ruta de la imagen
def getPath():
    path= 'images/monedas.jpg'
    return path 

# Se define la funcion getImage para leer la imagen desde la ruta especificada
# con el modo de color ch
def getImage(path,ch):
    image = cv2.imread(path,ch)
    return image

# Se define la funcion showImg para mostrar la imagen en una ventana con el nombre especificado
def showImg(nameW,img):
    cv2.imshow(nameW,img)

# Se define la funcion destroy
def destroy():
    cv2.destroyAllWindows()

# Se define la funcion sizeImg para obtener el alto y ancho de la imagen
def sizeImg(img):
    h,w = img.shape[:2]
    return h,w

# Se define la funcion mouseClick para manejar los eventos del raton. 
# Se guardan las coordenadas del clic inicial y final y establece badClick verdadero
def mouseClick(event,x,y,flags,param):
    global x1,y1,x2,y2, bandClick
    if(event == cv2.EVENT_LBUTTONDOWN):
        x1=x
        y1=y
    elif(event== cv2.EVENT_LBUTTONUP):
        x2=x
        y2=y
        bandClick=True

# Se define la funcion getRoi para obtener la region de interes de la imagen en funcion de las coordenas del clic
def getRoi(x1,y1,x2,y2,img):
    imgRoi= img[y1:y2,x1,x2]
    return imgRoi

# se define la binaryImg para binarizar la imagen en escala de grises utilizando un umbral u
def binaryImg(imgGray,u):
    ret, imgBinary = cv2.threshold(imgGray,u,255,cv2.THRESH_BINARY_INV)
    return imgBinary

# Se define la función nothing que no hace nada, se utiliza como una función de devolución de llamada para el rastreador.
def nothing(x):
    pass

# La función principal main() inicializa las ventanas, establece la devolución de llamada del ratón y crea un rastreador para el ajuste del umbral.
def main():
    global x1,y1,x2,y2,bandClick
    cv2.namedWindow("imgColor")
    cv2.namedWindow("imgGray")
    cv2.setMouseCallback("imgColor",mouseClick)
    cv2.createTrackbar('u1',"imgGray",0,255,nothing)
    # Cargamos la imagen en color y en escala de grises, y obtenemos su tamaño
    imgColor= getImage(getPath(),1)
    imgGray=getImage(getPath(),0)
    y2,x2= sizeImg(imgColor)

    # Se definen los umbrales con los que se van a segmentar los grupos
    umbral1=(70,99)
    umbral2=(100,124)
    umbral3=(125,161)

    # Se definen los grupos con la funcion .inRange
    grupo1 = cv2.inRange(imgGray,umbral1[0],umbral1[1])
    grupo2 = cv2.inRange(imgGray,umbral2[0],umbral2[1])
    grupo3 = cv2.inRange(imgGray,umbral3[0],umbral3[1])

    # Se colorean los grupos definidos con un color aleatorio con .random.randit
    colores=np.random.randint(0,255,size=(3,3))

    # Se crea una matriz de ceros del mismo tamaño y tipo que la imagen.
    #Esta matriz se utiliza para almacenar la imagen coloreada
    coloreado = np.zeros_like(imgColor)

    # Se recorren los pixeles de la imagen original, utilizando dos bloques anidados.
    # Para cada pixel se verifica a que grupo pertenece segun los resultados de la segmentacion.
    # Dependiendo del grupo al que pertenezca el pixel, se asigna un color correspondiente de la matriz colores a la posicion correspondiente en la matriz coloreado
    for i in range(imgColor.shape[0]):
        for j in range(imgColor.shape[1]):
            if grupo1[i,j]>0:
                coloreado[i,j]=colores[0]
            elif grupo2[i,j]>0:
                coloreado[i,j]=colores[1]
            elif grupo3[i,j]>0:
                coloreado[i,j]=colores[2]
    
    # Se muestra la imagen con los grupos coloreados
    showImg('Grupos coloreados',coloreado)
    while True:
        # Se muestran las imagenes a color y en escala de grises 
        showImg("imgColor",imgColor)
        showImg("imgGray",imgGray)
        # Si se hace click se muestra la region
        if(bandClick):
            imgRoi= getRoi(x1,y1,x2,y2,imgColor)
            showImg("imgRoi",imgRoi)
            bandClick=False
        
        # Se obtiene el valor del umbral del rastreador 
        u = cv2.getTrackbarPos('u1',"imgGray")
        # Se binariza la imagen en escala de grisese binariza la imagen en escala de grises
        imgBinary = binaryImg(imgGray,u)
        # Se muestra la imagen binarizada y se sale del bucle si se preciona
        showImg("imgBinary",imgBinary)
        # showImg(grupo1)
        # Se muestra la imagen binarizada y se sale del bucle si se presiona la tecla q
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
    destroy()
# Se llama a la funcion principal main
if __name__ == "__main__":
    main()




