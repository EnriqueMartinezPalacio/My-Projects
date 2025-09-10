

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np

class FruitClassifierApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Sistema de Clasificación de Frutas")

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.font_style = ("Arial", 10, "bold")

        self.contours = []
        self.current_image_index = 0
        self.current_roi_index = 0
        self.image_paths = []  # Lista para almacenar las rutas de las imágenes

        # Configurar la interfaz gráfica
        self.setup_ui()

    def setup_ui(self):
        frame_width = 300
        frame_height = 250

        # Marco para la visualización de la imagen original
        frame_original = tk.LabelFrame(self.window, text="Imagen Original", width=frame_width, height=frame_height, borderwidth=3, font=self.font_style)
        frame_original.place(x=25, y=40)
        self.label_original = tk.Label(frame_original)
        self.label_original.pack(expand=True, fill="both")

        # Marco para la imagen binarizada
        frame_binarized = tk.LabelFrame(self.window, text="Imagen Binarizada", width=frame_width, height=frame_height, borderwidth=3, font=self.font_style)
        frame_binarized.place(x=350, y=40)
        self.label_binarized = tk.Label(frame_binarized)
        self.label_binarized.pack(expand=True, fill="both")

        # Marco para la imagen con contornos
        frame_contours = tk.LabelFrame(self.window, text="Imagen con Contornos", width=frame_width, height=frame_height, borderwidth=3, font=self.font_style)
        frame_contours.place(x=675, y=40)
        self.label_contours = tk.Label(frame_contours)
        self.label_contours.pack(expand=True, fill="both")

        # Marco para los objetos clasificados
        frame_classified = tk.LabelFrame(self.window, text="Objetos Clasificados", width=frame_width, height=frame_height, borderwidth=3, font=self.font_style)
        frame_classified.place(x=25, y=320)
        self.label_classified = tk.Label(frame_classified)
        self.label_classified.pack(expand=True, fill="both")

        # Marco para el conteo de referencias
        frame_references = tk.LabelFrame(self.window, text="Conteo de Referencias", width=frame_width, height=frame_height, borderwidth=3, font=self.font_style)
        frame_references.place(x=350, y=320)
        self.label_references = tk.Label(frame_references, text="Limón: 0\nCebolla: 0\nPapa: 0\nTomate de Árbol: 0", justify=tk.LEFT, font=self.font_style)
        self.label_references.pack(expand=True, fill="both")

        # Botones de control
        frame_controls = tk.LabelFrame(self.window, text="Controles", width=frame_width, height=frame_height, borderwidth=3, font=self.font_style)
        frame_controls.place(x=675, y=320)
        self.btn_start = tk.Button(frame_controls, text="Inicio", font=self.font_style, background='green', command=self.start_classification)
        self.btn_start.pack(side=tk.TOP, pady=5)
        self.btn_next = tk.Button(frame_controls, text="Siguiente", font=self.font_style, background='gray', command=self.show_next_image)
        self.btn_next.pack(side=tk.TOP, pady=5)
        self.btn_continue = tk.Button(frame_controls, text="ROI", font=self.font_style, background='gray', command=self.show_next_roi)
        self.btn_continue.pack(side=tk.TOP, pady=5)
        self.btn_stop = tk.Button(frame_controls, text="Parar", font=self.font_style, background='red', command=self.window.quit)
        self.btn_stop.pack(side=tk.TOP, pady=5)

        # Carpeta que contiene las imágenes
        folder_path = "C:/Users/enri-/Desktop/10mo_Semestre/Vision_Artificial/Final/Imagenes/Verticales"  # Ruta a la carpeta Vertical
        self.image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(('.jpg', '.jpeg', '.png'))]

        if not self.image_paths:
            messagebox.showerror("Error", "No se encontraron imágenes en la carpeta especificada.")
            return

        # Cargar la primera imagen
        self.load_image()

    def load_image(self):
        image_path = self.image_paths[self.current_image_index]
        self.original_cv_image = cv2.imread(image_path)
        original_image = Image.open(image_path)
        original_image = original_image.resize((300, 250))
        self.original_photo = ImageTk.PhotoImage(original_image)
        self.label_original.configure(image=self.original_photo)

        # Binarizar la imagen original utilizando espacio de color HSV
        hsv_image = cv2.cvtColor(self.original_cv_image, cv2.COLOR_BGR2HSV)

        # Definir los límites de color para binarizar (por ejemplo, para blanco)
        lower_white = np.array([0, 56, 42])  # Bajo límite de blanco en HSV
        upper_white = np.array([178, 255, 255])  # Alto límite de blanco en HSV

        # Crear una máscara para el color blanco
        mask_white = cv2.inRange(hsv_image, lower_white, upper_white)

        # Aplicar la máscara a la imagen original para obtener la imagen binarizada
        binarized_image = cv2.bitwise_and(self.original_cv_image, self.original_cv_image, mask=mask_white)

        # Convertir la imagen binarizada a formato PIL para mostrarla en la interfaz
        binarized_pil_image = Image.fromarray(mask_white)
        binarized_pil_image = binarized_pil_image.resize((300, 250))
        binarized_photo = ImageTk.PhotoImage(binarized_pil_image)

        # Mostrar la imagen binarizada en la etiqueta de imagen binarizada
        self.label_binarized.image = binarized_photo
        self.label_binarized.configure(image=binarized_photo)

        # Convertir la imagen binarizada a escala de grises
        gray_binarized_image = cv2.cvtColor(binarized_image, cv2.COLOR_BGR2GRAY)

        # Encontrar contornos en la
                # imagen binarizada en escala de grises
        contours, _ = cv2.findContours(gray_binarized_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filtrar los contornos para obtener solo los más grandes
        min_contour_area = 1000
        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

        # Dibujar contornos en la copia de la imagen original
        self.image_with_contours = self.original_cv_image.copy()
        cv2.drawContours(self.image_with_contours, large_contours, -1, (0, 255, 0), 2)

        # Convertir la imagen con contornos a formato PIL para mostrarla en la interfaz
        contours_pil_image = Image.fromarray(cv2.cvtColor(self.image_with_contours, cv2.COLOR_BGR2RGB))
        contours_pil_image = contours_pil_image.resize((300, 250))
        contours_photo = ImageTk.PhotoImage(contours_pil_image)

        # Mostrar la imagen con contornos en la etiqueta de imagen con contornos
        self.label_contours.image = contours_photo
        self.label_contours.configure(image=contours_photo)

        # Guardar los contornos encontrados
        self.contours = large_contours
        self.current_roi_index = 0

    def start_classification(self):
        # Cargar la primera imagen y comenzar el proceso de clasificación
        self.load_image()

    def show_next_image(self):
        # Mostrar la siguiente imagen de la carpeta
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.load_image()

    def show_next_roi(self):
        if self.contours:
            if self.current_roi_index < len(self.contours):
                contour = self.contours[self.current_roi_index]
                x, y, w, h = cv2.boundingRect(contour)
                roi = self.original_cv_image[y:y+h, x:x+w]

                # Guardar la ROI como una imagen en la carpeta ROI
                roi_folder_path = "C:/Users/enri-/Desktop/10mo_Semestre/Vision_Artificial/Final/ROI"
                if not os.path.exists(roi_folder_path):
                    os.makedirs(roi_folder_path)
                
                roi_image_path = os.path.join(roi_folder_path, f"roi_{self.current_image_index}_{self.current_roi_index}.jpg")
                cv2.imwrite(roi_image_path, roi)
                
                # Convertir la ROI a formato PIL para mostrarla en la ventana de objetos clasificados
                roi_pil_image = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
                roi_pil_image = roi_pil_image.resize((300, 250))
                roi_photo = ImageTk.PhotoImage(roi_pil_image)

                # Mostrar la ROI en la etiqueta de imagen de objetos clasificados
                self.label_classified.configure(image=roi_photo)
                self.label_classified.image = roi_photo

                # Incrementar el índice de la ROI actual para mostrar la siguiente ROI la próxima vez que se presione el botón "Continuar"
                self.current_roi_index += 1
            else:
                messagebox.showinfo("Fin de las ROIs", "Se han mostrado todas las ROIs en esta imagen.")
        else:
            messagebox.showerror("Error", "No se encontraron contornos en la imagen actual.")

if __name__ == "__main__":
    window = tk.Tk()
    app = FruitClassifierApp(window)
    window.geometry("1000x600")
    window.mainloop()

