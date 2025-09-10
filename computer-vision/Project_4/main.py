import cv2
import time
# Se define la direccion del video
pathVideo = "videos/video.mp4"
def nothing(x):
    pass


# Definimos el main
def main():
    #Por medio del cv2.VideoCapture() leemos el video
    capture = cv2.VideoCapture(pathVideo)
    #Verifico que si se abra el video
    if not capture.isOpened():
        print("Error al abrir el video.")
        exit()
    #Defino mis indicadores, estos van a ser prev_pixel(pixel anterior)
    #current_pixel(que es mi pixel actual) y mi contador coins
    prev_pixel = False
    current_pixel = False
    coins = 0
    #Definimos los trackbar para establecer cuales son los umbrales de la mascara a utilizar
    # El time .sleep es por que necesitbamos este tiempo paque leyera bien 
    time.sleep(2)
    cv2.namedWindow("frameHsv")
    cv2.createTrackbar('Hlower',"frameHsv",0,255,nothing)
    cv2.createTrackbar('Hupper',"frameHsv",0,255,nothing)
    cv2.createTrackbar('Slower',"frameHsv",0,255,nothing)
    cv2.createTrackbar('Supper',"frameHsv",0,255,nothing)
    cv2.createTrackbar('Vlower',"frameHsv",0,255,nothing)
    cv2.createTrackbar('Vupper',"frameHsv",0,255,nothing)
    #Bajo el condicional visto en clase abrimos el video 
    #y decimos que miestras que haya un frame adelante el ciclo while va a funcionar
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        Hmin=cv2.getTrackbarPos('Hlower',"frameHsv")
        Hmax=cv2.getTrackbarPos('Hupper','frameHsv')
        Smin=cv2.getTrackbarPos('Slower','frameHsv')
        Smax=cv2.getTrackbarPos('Supper','frameHsv')
        Vmin=cv2.getTrackbarPos('Vlower','frameHsv')
        Vmax=cv2.getTrackbarPos('Vupper','frameHsv')
        
        #print(Hmin,Hmax)
        # Redimensionamos el fotograma al nuevo tamaño
        frame = cv2.resize(frame, (640, 480))

        # Convertimos el fotograma a HSV
        framHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        framBinary=cv2.inRange(framHsv,(Hmin,Smin,Vmin),(Hmax,Smax,Vmax))

        # Definimos los límites de color para detectar el blanco
        lower_white = (0, 0, 90)
        upper_white = (193, 255, 255)

        # Creamos una máscara para el color blanco
        mask = cv2.inRange(framHsv, lower_white, upper_white)

        # Verificar la posición de los píxeles en la barrera(en el medio del video)
        prev_pixel = current_pixel
        current_pixel = mask[320, 240] > 0

        # Contar una moneda cuando se cumple la condición especificada
        if prev_pixel and not current_pixel:# El condicinal es que cunado la moneda anterior sea blanca y la actual negra, me va a contar +1
            coins += 1

        # Mostrar el fotograma original
        cv2.imshow("Frame", frame)
        #cv2.imshow("FrameHSV",framBinary)
        # Mostrar el fotograma con la máscara aplicada
        cv2.imshow("Mask", mask)

        

        # Salir del bucle si se presiona 'q'
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Libera los recursos y cierra las ventanas
    capture.release()
    cv2.destroyAllWindows()

    print("Número de monedas que pasaron:", coins)

if __name__ == "__main__":
    main()
