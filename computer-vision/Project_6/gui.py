import cv2
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Zoom Dinámico de ROI")
        self.width = 800
        self.height = 600
        self.master.geometry(f"{self.width}x{self.height}")
        self.pack()

        # Variables para almacenar los paths de las imágenes y el factor de escala
        self.image_path = tk.StringVar()
        self.scale_factor = tk.DoubleVar(value=0.4)

        # Variables para almacenar la imagen binarizada y el factor de zoom
        self.binary_image_path = ""
        self.zoom_factor = tk.DoubleVar(value=1.0)

        # Variables para almacenar los puntos de la región de interés (ROI)
        self.roi_x1 = 0
        self.roi_y1 = 0
        self.roi_x2 = 0
        self.roi_y2 = 0

        # Variables para almacenar los puntos de los dos puntos seleccionados por el médico
        self.point1 = None
        self.point2 = None

        self.create_widgets()

    def create_widgets(self):
        # Título "IMAGEN REAL"
        self.lblRealImageTitle = tk.Label(self.master, text="IMAGEN REAL", font=("Arial", 12, "bold"))
        self.lblRealImageTitle.place(x=20, y=0)

        # Label para la imagen real
        self.lblRealImage = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblRealImage.place(x=20, y=20)

        # Título "IMAGEN BINARIZADA"
        self.lblBinaryImageTitle = tk.Label(self.master, text="IMAGEN BINARIZADA", font=("Arial", 12, "bold"))
        self.lblBinaryImageTitle.place(x=20, y=180)

        # Label para la imagen binarizada
        self.lblBinaryImage = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblBinaryImage.place(x=20, y=200)

        # Título "ROI and ZOOM"
        self.lblROIAndZoomTitle = tk.Label(self.master, text="ROI and ZOOM", font=("Arial", 12, "bold"))
        self.lblROIAndZoomTitle.place(x=420, y=0)

        # Canvas para la región de interés (ROI) con zoom
        self.canvasROI = tk.Canvas(self.master, borderwidth=2, relief="solid", width=200, height=200)
        self.canvasROI.place(x=420, y=20)

        # Slider para el factor de zoom
        self.zoom_slider = tk.Scale(self.master, from_=1, to=10, resolution=0.1, orient=tk.HORIZONTAL, label="Factor de Zoom", variable=self.zoom_factor, command=self.update_zoom)
        self.zoom_slider.place(x=20, y=450)

        # Botón para cargar la imagen real y binarizarla
        self.btnLoadImage = tk.Button(self.master, text="Cargar y Binarizar", command=self.load_and_binarize_image)
        self.btnLoadImage.place(x=20, y=500)

        # Texto e input para el nombre de la imagen
        self.lblImageName = tk.Label(self.master, text="Ingrese el nombre de la imagen:")
        self.lblImageName.place(x=20, y=550)
        self.entryImageName = tk.Entry(self.master, textvariable=self.image_path)
        self.entryImageName.place(x=200, y=550)

        # Texto e input para la escala de la imagen
        self.lblScale = tk.Label(self.master, text="Escala de la imagen(0-2):")
        self.lblScale.place(x=20, y=580)
        self.entryScale = tk.Entry(self.master, textvariable=self.scale_factor)
        self.entryScale.place(x=200, y=580)

        # Asignar eventos de ratón a la imagen binarizada
        self.lblBinaryImage.bind("<Button-1>", self.mouseClick)
        self.lblBinaryImage.bind("<B1-Motion>", self.mouseClick)
        self.lblBinaryImage.bind("<ButtonRelease-1>", self.mouseClick)

        # Botones para aplicar filtros espaciales y morfológicos
        self.median_blur_button = tk.Button(self.master, text="Median Blur", command=self.apply_median_blur)
        self.median_blur_button.place(x=300, y=500)

        self.erode_button = tk.Button(self.master, text="Erode", command=self.apply_erode)
        self.erode_button.place(x=400, y=500)

        # Botón para cargar configuraciones
        self.load_settings_button = tk.Button(self.master, text="Cargar Configuraciones")
        self.load_settings_button.place(x=500, y=550)

        # Botón para salir de la interfaz gráfica
        self.exit_button = tk.Button(self.master, text="Salir", command=self.confirm_exit)
        self.exit_button.place(x=640, y=550)

    def load_and_binarize_image(self):
        # Obtener el nombre de la imagen y la escala
        image_name = self.image_path.get()
        scale_factor = self.scale_factor.get()

        # Ruta completa de la imagen
        image_path = os.path.join("images", image_name)

        # Cargar la imagen real
        real_image = cv2.imread(image_path)
        if real_image is None:
            print(f"No se pudo cargar la imagen {image_path}")
            return

        # Redimensionar la imagen según la escala
        scaled_image = cv2.resize(real_image, None, fx=scale_factor, fy=scale_factor)

        # Convertir la imagen a escala de grises
        gray_image = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)

        # Binarizar la imagen
        _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

        # Mostrar la imagen real en el primer label
        self.real_image_tk = self.convert_image_to_tk(scaled_image)
        self.lblRealImage.configure(image=self.real_image_tk)
        self.lblRealImage.image = self.real_image_tk

        # Mostrar la imagen binarizada en el segundo label
        self.binary_image_tk = self.convert_image_to_tk(binary_image)
        self.lblBinaryImage.configure(image=self.binary_image_tk)
        self.lblBinaryImage.image = self.binary_image_tk

        # Almacenar la ruta de la imagen binarizada
        self.binary_image_path = image_path

    def apply_erode(self):
        # Aplicar la operación de erosión a la imagen binarizada
        binary_image = cv2.imread(self.binary_image_path, cv2.IMREAD_GRAYSCALE)
        kernel = np.ones((5, 5), np.uint8)
        eroded_image = cv2.erode(binary_image, kernel, iterations=1)
        self.show_image(eroded_image, self.lblBinaryImage)

    def apply_median_blur(self):
        # Aplicar el filtro de mediana a la imagen binarizada
        binary_image = cv2.imread(self.binary_image_path, cv2.IMREAD_GRAYSCALE)
        blurred_image = cv2.medianBlur(binary_image, 5)
        self.show_image(blurred_image, self.lblBinaryImage)

    def show_image(self, img, label):
        # Mostrar la imagen en un label
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        label.config(image=img_tk)
        label.image = img_tk

    def confirm_exit(self):
        # Confirmar la salida de la aplicación
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            self.master.destroy()

    def convert_image_to_tk(self, image):
        # Convertir la imagen para su uso en tkinter
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image=image_pil)
        return image_tk

    def mouseClick(self, event):
        # Manejar los eventos de ratón en la imagen binarizada
        if event.type == tk.EventType.ButtonPress:
            self.roi_x1 = event.x
            self.roi_y1 = event.y
        elif event.type == tk.EventType.Motion:
            self.roi_x2 = event.x
            self.roi_y2 = event.y
            self.update_zoom(None)
        elif event.type == tk.EventType.ButtonRelease:
            self.update_zoom(None)

    def update_zoom(self, _):
        # Actualizar el zoom en la región de interés (ROI)
        if self.binary_image_path:
            roi_image = self.get_roi_image()
            if roi_image is not None:
                # Obtener las dimensiones de la imagen binarizada
                binary_image = cv2.imread(self.binary_image_path, cv2.IMREAD_GRAYSCALE)
                binary_height, binary_width = binary_image.shape

                # Verificar que los puntos de la ROI estén dentro de los límites de la imagen
                roi_x1 = max(0, min(self.roi_x1, binary_width - 1))
                roi_y1 = max(0, min(self.roi_y1, binary_height - 1))
                roi_x2 = max(0, min(self.roi_x2, binary_width - 1))
                roi_y2 = max(0, min(self.roi_y2, binary_height - 1))

                # Redimensionar la ROI si los puntos están dentro de los límites
                if roi_x1 != roi_x2 and roi_y1 != roi_y2:
                    roi_image = binary_image[roi_y1:roi_y2, roi_x1:roi_x2]
                    zoom_factor = self.zoom_factor.get()
                    zoomed_roi_height = int(roi_image.shape[0] * zoom_factor)
                    zoomed_roi_width = int(roi_image.shape[1] * zoom_factor)
                    zoomed_roi_image = cv2.resize(roi_image, (zoomed_roi_width, zoomed_roi_height), interpolation=cv2.INTER_NEAREST)
                    zoomed_roi_tk = self.convert_image_to_tk(zoomed_roi_image)

                    # Limpiar el canvas antes de dibujar la nueva imagen
                    self.canvasROI.delete(tk.ALL)

                    # Dibujar la imagen en el canvas
                    self.canvasROI.create_image(0, 0, anchor=tk.NW, image=zoomed_roi_tk)
                    self.canvasROI.image = zoomed_roi_tk

                    # Dibujar la línea entre los dos puntos seleccionados
                    if self.point1 is not None and self.point2 is not None:
                        self.canvasROI.create_line(self.point1[0], self.point1[1], self.point2[0], self.point2[1], fill="red")

    def get_roi_image(self):
        # Obtener la región de interés (ROI) de la imagen binarizada
        if self.binary_image_path:
            binary_image = cv2.imread(self.binary_image_path, cv2.IMREAD_GRAYSCALE)
            roi_image = binary_image[self.roi_y1:self.roi_y2, self.roi_x1:self.roi_x2]
            return roi_image
        else:
            return None

        

def main():
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()


