import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import socket
import threading

import runCamera
import reportLog

class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.logReport = reportLog.ReportLog()
        self.camera = runCamera.RunCamera(1)
        self.master = master
        self.width = 1500
        self.height = 660
        self.master.geometry("%dx%d" % (self.width, self.height))
        self.pack()
        self.lblCoins = {}
        self.createWidgets()
        self.logReport.logger.info("GUI Created")
        self.paused = False
        self.coins = {"Moneda de $1000": 0, "Moneda de $500": 0, "Moneda de $200": 0, "Moneda de $100": 0, "Moneda de $50": 0}
        self.servidor_ip = '172.20.10.11'
        self.servidor_puerto = 80 
        self.updateCoinLabels()
        self.updateTotalCoinsValueLabel()
        self.master.mainloop()

    def createWidgets(self):
        self.fontText = font.Font(family='Helvetica', size=8, weight='normal')

        # Crear marcos para los videos
        self.lblVideoOriginal = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideoOriginal.place(x=20, y=25)
        self.lblVideoBinarizado = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideoBinarizado.place(x=700, y=25)

        # Crear etiquetas
        self.lblNameCameraOriginal = tk.Label(self.master, text="Video Original", fg='#000000', font=self.fontText)
        self.lblNameCameraOriginal.place(x=20, y=5)

        self.lblNameCameraBinarizado = tk.Label(self.master, text="Video Binarizado", fg='#000000', font=self.fontText)
        self.lblNameCameraBinarizado.place(x=700, y=5)

        self.lblTotalCoinsValue = tk.Label(self.master, text="Valor total de las monedas: 0", fg='#000000', font=self.fontText)
        self.lblTotalCoinsValue.place(x=150, y=600)

        # Crear botones
        buttons = [("Iniciar", self.initCameraProcess, 100, 530),
                   ("Parar", self.stopCameraProcess, 100, 560),
                   ("Pausa", self.pauseCamera, 250, 530),
                   ("Continuar", self.continueCamera, 250, 560)]

        for text, command, x, y in buttons:
            btn = tk.Button(self.master, text=text, bg="#007A39", fg="#FFFFFF", width=12, command=command)
            btn.place(x=x, y=y)

        # Crear etiquetas de monedas
        coin_labels = ["Moneda de $1000", "Moneda de $500", "Moneda de $200", "Moneda de $100", "Moneda de $50"]
        for i, label in enumerate(coin_labels):
            self.lblCoins[label] = tk.Label(self.master, text=f"{label}: 0", fg='#000000', font=self.fontText)
            self.lblCoins[label].place(x=450, y=515 + i * 25)

    def updateTotalCoinsValueLabel(self):
        total_coins_value = sum([self.coins[key] * value for key, value in {"Moneda de $1000": 1000, "Moneda de $500": 500, "Moneda de $200": 200, "Moneda de $100": 100, "Moneda de $50": 50}.items()])
        self.lblTotalCoinsValue.config(text=f"Valor total de las monedas: {total_coins_value}")

    def updateCoinLabels(self):
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
        if area > 28000:
            self.enviarComandoServo("1000", 90)
            return "Moneda de $1000"
        elif area > 24000:
            self.enviarComandoServo("200", 45)
            return "Moneda de $200"
        elif area > 22000:
            self.enviarComandoServo("500", 45)
            return "Moneda de $500"
        elif area > 16000:
            self.enviarComandoServo("100", 45)
            return "Moneda de $100"
        elif area > 15000:
            self.enviarComandoServo("50", 45)
            return "Moneda de 50 centavos"

    def enviarComandoServo(self, tipo_moneda, grados):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.servidor_ip, self.servidor_puerto))
            mensaje = f"{tipo_moneda},{grados}\n"
            s.sendall(mensaje.encode())

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

                if self.paused:
                    return

                contours, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area < 15000:
                        continue
                    tipo_moneda = self.clasificarMonedas(area)

                    if tipo_moneda in self.coins:
                        self.coins[tipo_moneda] += 1
                    else:
                        self.coins[tipo_moneda] = 1

                self.updateCoinLabels()
                self.updateTotalCoinsValueLabel()

                imgArrayBinarizado = Image.fromarray(mascara)
                imgTkBinarizado = ImageTk.PhotoImage(image=imgArrayBinarizado)
                self.lblVideoBinarizado.configure(image=imgTkBinarizado)
                self.lblVideoBinarizado.image = imgTkBinarizado

            self.lblVideoOriginal.after(10, self.getFrameInLabel)
        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabel" + str(e))

def main():
    root = tk.Tk()
    root.title("My first GUI")
    appRunCamera = App(master=root)


