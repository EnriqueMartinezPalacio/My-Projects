import cv2
import time

# Se define la dirección del video
pathVideo = "videos/video_1_7.avi"
#pathVideo=1
def nothing(x):
    pass

# Función para clasificar el tamaño de las monedas
def clasificarMonedas(area):
    print(f"Area:{area}")
    if area > 28000:
        return "Moneda de $1000"
    elif area > 24000:
        return "Moneda de $200"
    elif area > 22000:
        return "Moneda de $500"
    elif area > 21000:
        return "Moneda de $100"
    elif area>18000:
        return "Moneda de 50"

# Definimos el main
def main():
    # Por medio del cv2.VideoCapture() leemos el video
    capture = cv2.VideoCapture(pathVideo)#,cv2.CAP_DSHOW)

    # Verifico que si se abra el video
    if not capture.isOpened():
        print("Error al abrir el video.")
        exit()

    # Defino mis indicadores
    pixel_anterior = False
    pixel_actual = False
    coins = {}

    # Definimos los trackbars para establecer cuales son los umbrales de la mascara a utilizar
    time.sleep(2)
    cv2.namedWindow("frameHsv")
    cv2.createTrackbar('Hlower', "frameHsv", 0, 255, nothing)
    cv2.createTrackbar('Hupper', "frameHsv", 0, 255, nothing)
    cv2.createTrackbar('Slower', "frameHsv", 0, 255, nothing)
    cv2.createTrackbar('Supper', "frameHsv", 0, 255, nothing)
    cv2.createTrackbar('Vlower', "frameHsv", 0, 255, nothing)
    cv2.createTrackbar('Vupper', "frameHsv", 0, 255, nothing)

    # Bajo el condicional visto en clase abrimos el video
    # y decimos que mientras que haya un frame adelante el ciclo while va a funcionar
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        Hmin = cv2.getTrackbarPos('Hlower', "frameHsv")
        Hmax = cv2.getTrackbarPos('Hupper', 'frameHsv')
        Smin = cv2.getTrackbarPos('Slower', 'frameHsv')
        Smax = cv2.getTrackbarPos('Supper', 'frameHsv')
        Vmin = cv2.getTrackbarPos('Vlower', 'frameHsv')
        Vmax = cv2.getTrackbarPos('Vupper', 'frameHsv')

        frame = cv2.resize(frame, (640, 480))

        # Convertimos el fotograma a HSV
        framHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV | cv2.THRESH_OTSU)

        # Definimos los límites de color para detectar el blanco
        # lower_white = (0, 0, 90)
        # upper_white = (200, 255, 255)

        lower_white = (0, 0, 110)
        upper_white = (200, 255, 255)

        # lower_white = (Hmin, Smin, Vmin)
        # upper_white = (Hmax, Smax, Vmax)

        # Creamos una máscara para el color blanco
        mascara = cv2.inRange(framHsv, lower_white, upper_white)

        # Verificar la posición de los píxeles en la barrera (en el medio del video)
        pixel_anterior = pixel_actual
        pixel_actual = mascara[320, 240] > 0

        # Contar una moneda cuando se cumple la condición especificada
        if pixel_anterior and not pixel_actual:
            # Encuentra los contornos de las monedas
            contours, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                # Calcula el área de cada contorno
                area = cv2.contourArea(cnt)
                # Clasifica la moneda según su tamaño
                if area <15000:
                    continue
                tipo_moneda = clasificarMonedas(area)
                # Agrega la moneda al diccionario de monedas
                if tipo_moneda in coins:
                    coins[tipo_moneda] += 1
                else:
                    coins[tipo_moneda] = 1

        # Mostrar el fotograma original
        cv2.imshow("Frame", frame)
        # Mostrar el fotograma con la máscara aplicada
        cv2.imshow("ImgMascara", mascara)

        # Salir del bucle si se presiona 'q'
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Libera los recursos y cierra las ventanas
    capture.release()
    cv2.destroyAllWindows()

    # Imprimir el número de cada tipo de moneda detectada
    print("Número de monedas detectadas:")
    for tipo, cantidad in coins.items():
        print(tipo + ":", cantidad)
    valor_moneda = {
        "Moneda de $1000": 1000,
        "Moneda de $500": 500,
        "Moneda de $200": 200,
        "Moneda de $100": 100,
        "Moneda de $50": 50
    }

    # Calcular el valor total de las monedas
    valor_total = sum(cantidad * valor_moneda[tipo] for tipo, cantidad in coins.items())

    # Imprimir el valor total de las monedas
    print("Valor total de las monedas:", valor_total)

if __name__ == "__main__":
    main()
