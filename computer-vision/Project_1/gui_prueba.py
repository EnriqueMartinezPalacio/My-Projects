import cv2
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from PIL import Image, ImageTk
import socket

import reportLog
import runCamera
import gui

class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.logReport = reportLog.ReportLog()
        #self.camera=runCamera.RunCamera(1)
        self.camera = runCamera.RunCamera(src="C:/Users/enri-/Desktop/10mo_Semestre/Vision_Artificial/Actividad_3/videos/video.mp4", name="video_1")

        self.master = master
        self.width = 1500
        self.height = 660
        self.master.geometry("%dx%d" % (self.width, self.height))
        self.pack()
        self.panel = None
        self.lblCoins = {}  # Inicializar el diccionario lblCoins
        self.createFrameZeros()
        self.createWidgets()
        self.logReport.logger.info("GUI Created")
        self.pixel_anterior = False
        self.pixel_actual = False
        self.paused = False  # Nuevo atributo para controlar el estado de la cámara
        self.coins = {"Moneda de $1000": 0, "Moneda de $500": 0, "Moneda de $200": 0, "Moneda de $100": 0, "Moneda de $50": 0}
        self.servidor_ip = '172.20.10.11' # Dirección IP de la ESP32 (ajusta según tu configuración)
        self.servidor_puerto = 80 
        self.updateCoinLabels()
        self.updateTotalCoinsValueLabel()
        self.processed_coins=set()
        #self.enviarComandoServo()
        self.master.mainloop()

    # def valorTotal(self):
    #     self

    def createFrameZeros(self):
        self.lblVideoOriginal = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideoOriginal.place(x=20, y=25)
        self.lblVideoBinarizado = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideoBinarizado.place(x=700, y=25)

    def createWidgets(self):
        self.fontText = font.Font(family='Helvetica', size=8, weight='normal')

        self.lblNameCameraOriginal = tk.Label(self.master, text="Video Original", fg='#000000', font=self.fontText)
        self.lblNameCameraOriginal.place(x=20, y=5)

        self.lblNameCameraBinarizado = tk.Label(self.master, text="Video Binarizado", fg='#000000', font=self.fontText)
        self.lblNameCameraBinarizado.place(x=700, y=5)

        self.btnInitCamera = tk.Button(self.master, text="Iniciar", bg="#007A39", fg="#FFFFFF", width=12, command=self.initCameraProcess)
        self.btnInitCamera.place(x=100, y=530)

        self.btnStopCamera = tk.Button(self.master, text="Parar", bg="#007A39", fg="#FFFFFF", width=12, command=self.stopCameraProcess)
        self.btnStopCamera.place(x=100, y=560)

        self.btnPauseCamera = tk.Button(self.master, text="Pausa", bg="#007A39", fg="#FFFFFF", width=12, command=self.pauseCamera)
        self.btnPauseCamera.place(x=250, y=530)

        self.btnContinueCamera = tk.Button(self.master, text="Continuar", bg="#007A39", fg="#FFFFFF", width=12, command=self.continueCamera)
        self.btnContinueCamera.place(x=250, y=560)

        self.lblTotalCoinsValue = tk.Label(self.master, text="Valor total de las monedas: 0", fg='#000000', font=self.fontText)
        self.lblTotalCoinsValue.place(x=150, y=600)


        # Crear etiquetas para mostrar la cantidad de monedas de cada categoría
        coin_labels = ["Moneda de $1000", "Moneda de $500", "Moneda de $200", "Moneda de $100", "Moneda de $50"]
        for i, label in enumerate(coin_labels):
            self.lblCoins[label] = tk.Label(self.master, text=f"{label}: 0", fg='#000000', font=self.fontText)
            self.lblCoins[label].place(x=450, y=515 + i * 25)


    def updateTotalCoinsValueLabel(self):
        # Obtener el valor total de las monedas
        
        #valor_total = sum(cantidad * valor_moneda[tipo] for tipo, cantidad in self.coins.items())

        total_coins_value = sum([self.coins["Moneda de $1000"] * 1000, self.coins["Moneda de $500"] * 500, self.coins["Moneda de $200"] * 200, self.coins["Moneda de $100"] * 100, self.coins["Moneda de $50"] * 50])

        # Actualizar el texto de la etiqueta con el valor total de las monedas
        self.lblTotalCoinsValue.config(text=f"Valor total de las monedas: {total_coins_value}")

    def updateCoinLabels(self):
        # Actualizar el texto de las etiquetas de las monedas con la cantidad actual
        for label, count in self.coins.items():
            self.lblCoins[label].config(text=f"{label}: {count}")

    def initCameraProcess(self):
        self.camera.start()
        self.getFrameInLabel()

    def stopCameraProcess(self):
        self.camera.stop()

    def pauseCamera(self):
        self.paused = True

    def continueCamera(self):
        self.paused = False
        self.getFrameInLabel()

    def clasificarMonedas(self, area):
        print(area)
        if area > 26000:
            self.enviarComandoServo("1000", 90)
            return "Moneda de $1000"
        elif area > 23000:
            self.enviarComandoServo("200", 60)
            return "Moneda de $200"
        elif area > 22000:
            self.enviarComandoServo("500", 45)
            return "Moneda de $500"
        elif area > 15000:
            self.enviarComandoServo("100", 30)
            return "Moneda de $100"
        elif area > 11000:
            self.enviarComandoServo("50", 50)
            return "Moneda de $50"

        
        
    def enviarComandoServo(self, tipo_moneda, grados):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.servidor_ip, self.servidor_puerto))
                mensaje = f"{tipo_moneda},{grados}\n"
                s.sendall(mensaje.encode())
        except Exception as e:
            print("Error al enviar comando al servo:", e)    
        

    def getFrameInLabel(self):
        try:
            if self.camera.grabbed and self.camera.frame is not None and not self.paused:
                frameCamera = self.camera.frame
                frame_original = cv2.resize(frameCamera, (640, 480))
                frame_original = cv2.cvtColor(frame_original, cv2.COLOR_BGR2RGB)
                imgArrayOriginal = Image.fromarray(frame_original)
                imgTkOriginal = ImageTk.PhotoImage(image=imgArrayOriginal)
                self.lblVideoOriginal.configure(image=imgTkOriginal)
                self.lblVideoOriginal.image = imgTkOriginal

                framRGB = cv2.cvtColor(frameCamera, cv2.COLOR_BGR2HSV)

                lower_white = (0, 0, 140)
                upper_white = (229,255,255)
                mascara = cv2.inRange(framRGB, lower_white, upper_white)
                mascara = cv2.resize(mascara, (640, 480))

                self.pixel_anterior = self.pixel_actual
                self.pixel_actual = mascara[325, 245] > 0
                if self.pixel_anterior and not self.pixel_actual:
                    contours, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        print(area)
                        if area<15000:
                            continue
                        
                        tipo_moneda = self.clasificarMonedas(area)
                        if tipo_moneda in self.coins:
                            self.coins[tipo_moneda] += 1
                            self.processed_coins.add(tipo_moneda)
                        else:
                            self.coins[tipo_moneda] = 1
                    self.updateCoinLabels()
                    self.updateTotalCoinsValueLabel()
                else:
                    self.processed_coins=set()

                imgArrayBinarizado = Image.fromarray(mascara)
                imgTkBinarizado = ImageTk.PhotoImage(image=imgArrayBinarizado)
                self.lblVideoBinarizado.configure(image=imgTkBinarizado)
                self.lblVideoBinarizado.image = imgTkBinarizado

            self.lblVideoOriginal.after(10, self.getFrameInLabel)
        except Exception as e:
            print("Error in getFrameInLabel:",e)

def main():
    root = tk.Tk()
    root.title("My first GUI")
    appRunCamera = App(master=root)



