# Código para contar las barras BLANCAS de la imagen barras.png
# y para contar la distancia en pixeles entre estas
# 
# -----------------------------------------------------------------------------------------------------------------------------------------------#

import numpy as np
import cv2

def ruta(RUTA):  # Función para sacar la ruta de la imagen
    path=RUTA
    return path

def crearIMG(path, canal):  #Se crea una imagen llamada "imagen"
    imagen = cv2.imread(path, canal)
    return imagen

def mostrarIMG(NombreVentana,imagen): #Se crea la ventana y se muestra la imagen
    cv2.imshow(NombreVentana,imagen)
    
def destruir():  # Destruir ventanas
    cv2.destroyAllWindows()
    
def contar_barras(imagen):  # Con esta función se cuentan las barras separadas por espacios negros
    contador = 0
    global mitadY
    mitadY = round(imagen.shape[0]/2) #Se saca un aproximado de dónde queda la mitad de la imagen para contar los pixeles en esa linea central horizontal
  
    for i in range(1,imagen.shape[1]-1): # Recorremos toda la fila en X 
        if(imagen[mitadY,i-1] == 0 and imagen[mitadY,i+1] == 255 and imagen[mitadY,i] == 255): #Si el pixel anterior es negro y el pixel siguiente es diferente, se cuenta como barra
            contador += 1
    
    return contador

def binaryImg(imagenGray,U1):
    imgBinaria = cv2.threshold(imagenGray, U1, 255, cv2.THRESH_BINARY)
    return imgBinaria

def contarEspacio(imagen, numerodebarras): # Contar distancia entre barras BLANCAS
    global distancias
    global contadorpxl
    distancias = [] #Lista donde guardamos las distancias entre barras
    contadorpxl = 0 # Contador de pixeles
    
    for i in range(1,imagen.shape[1]-1): # Recorremos horizontalmente la imagen
        
        if(imagen[mitadY,i-1] == 255 and imagen[mitadY,i] == 0 ): # Si el pixel anterior es blanco y el actual es negro
            contadorpxl = 0 # Reiniciamos el contador
            j=i # Creamos una variable j como contador para un ciclo
            while (imagen[mitadY,j] == 0) : # mientras que el pixel actual sea negro, iremos recorriendo la imagen
                contadorpxl +=1 # Sumamos  1 al contador de pixeles
                j +=1 # Sumamos 1 al contador
                if(j==imagen.shape[1]): # Si llegamos al límite de la imagen, rompemos el ciclo
                    break
                
            distancias.append(contadorpxl) # Agregamos el contador, o sea, la cantidad de pxeles a la lista
            
    if(len(distancias)>numerodebarras): # Esto es para corregir un error del código, en el que cuenta la distancia entre la última barra y el "infinito"
        distancias.pop(-1)
    
    
    for i in range(1, len(distancias)): #Esto es solo para imprimir las distancias
        print("La distancia entre la barra ",i,"y la barra ",i+1,"es:", distancias[i-1], "pixeles")
    return(distancias)


def main():
    
    path = ruta("images/barras.png")
    imagen= crearIMG(path,0)
    mostrarIMG("Imagen",imagen )
    
    ret, imgbinaria= binaryImg(imagen,200)
    mostrarIMG("Imagen binarizada",imgbinaria) 
    
    cantidad_de_barras = contar_barras(imgbinaria)
    print("En la imagen hay", cantidad_de_barras, "barras")
    
    contarEspacio(imgbinaria,cantidad_de_barras)
    cv2.waitKey(0)
    destruir()
    
if __name__ == main():
    main()