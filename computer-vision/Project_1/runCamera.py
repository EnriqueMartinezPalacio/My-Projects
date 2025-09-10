import reportLog
import cv2
import threading
import numpy as np
import time
from PIL import Image
from PIL import ImageTk
class RunCamera():
    def __init__(self, src=0, name="CameraThread"):
        self.name = name
        self.src = src
        self.capture = None
        self.grabbed = None
        self.frame = None

    def start(self):
        try:
            self.capture = cv2.VideoCapture(self.src)#,cv2.CAP_DSHOW)
            self.grabbed, self.frame = self.capture.read()
            if self.capture.isOpened():
                self.cameraThread = threading.Thread(target=self.get, name=self.name, daemon=True)
                self.cameraThread.start()
        except Exception as e:
            print("Error runCamera start:", str(e))

    def stop(self):
        try: 
            if self.capture.isOpened():
                self.capture.release()
                self.frame = np.zeros_like(self.frame)
        except Exception as e:
            print("Error runCamera stop:", str(e))

    def get(self):
        try:
            while  self.grabbed:
                self.grabbed, self.frame = self.capture.read()
                if not self.grabbed:
                    break
                time.sleep(0.05)  # Espera 100 milisegundo, esto es para realentizar el video
        except Exception as e:
            print("Error get frame:", str(e))

    def getCapture(self):
        return self.capture
