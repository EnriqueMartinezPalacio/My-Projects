import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ultralytics import YOLO
import cv2

class YOLOInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Interfaz")

        self.model = YOLO("C:/Users/enri-/Desktop/Tesis/Dedos/best.pt")
        
        self.cap = cv2.VideoCapture(0)
        
        self.button_frame = ttk.Frame(root)
        self.button_frame.grid(row=2, column=3, pady=10)

        self.start_button = ttk.Button(self.button_frame, text="Iniciar", command=self.start_detection)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(self.button_frame, text="Detener", command=self.stop_detection, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)
        
        self.counter_frame = ttk.Frame(root, width=200, height=480)
        self.counter_frame.grid(row=0, column=3, padx=5, pady=5)
        self.counter_frame.grid_propagate(False)  # Prevenir que el frame cambie de tamaño
        
        # Labels en una sola columna
        self.dedos_label = ttk.Label(self.counter_frame, text="Dedos detectados: 0")
        self.dedos_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        
        self.clases_label = ttk.Label(self.counter_frame, text="Clases detectadas: 0")
        self.clases_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        
        self.manos_label = ttk.Label(self.counter_frame, text="Manos detectadas: 0")
        self.manos_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")
        
        
        self.area_promedio_label = ttk.Label(self.counter_frame, text="Área promedio: 0")
        self.area_promedio_label.grid(row=4, column=0, padx=5, pady=2, sticky="w")
        
        self.confianza_promedio_label = ttk.Label(self.counter_frame, text="Confianza promedio: 0")
        self.confianza_promedio_label.grid(row=5, column=0, padx=5, pady=2, sticky="w")
        

        self.manos_clase_1_label = ttk.Label(self.counter_frame, text="Manos con clase 1: 0")
        self.manos_clase_1_label.grid(row=7, column=0, padx=5, pady=2, sticky="w")
        
        self.manos_clase_2_label = ttk.Label(self.counter_frame, text="Manos con clase 2: 0")
        self.manos_clase_2_label.grid(row=8, column=0, padx=5, pady=2, sticky="w")
        
        self.manos_clase_3_label = ttk.Label(self.counter_frame, text="Manos con clase 3: 0")
        self.manos_clase_3_label.grid(row=9, column=0, padx=5, pady=2, sticky="w")
        
        self.manos_clase_4_label = ttk.Label(self.counter_frame, text="Manos con clase 4: 0")
        self.manos_clase_4_label.grid(row=10, column=0, padx=5, pady=2, sticky="w")
        
        self.manos_clase_5_label = ttk.Label(self.counter_frame, text="Manos con clase 5: 0")
        self.manos_clase_5_label.grid(row=11, column=0, padx=5, pady=2, sticky="w")
        
        self.realtime_frame = ttk.LabelFrame(root, text="Detalle de la imagen", width=640, height=480)
        self.realtime_frame.grid(row=0, column=1, padx=5, pady=5)
        self.realtime_frame.grid_propagate(False)  # Prevenir que el frame cambie de tamaño
        
        self.realtime_label = ttk.Label(self.realtime_frame)
        self.realtime_label.pack()
        
        self.detail_frame = ttk.LabelFrame(root, text="Detección en tiempo real ", width=640, height=480)
        self.detail_frame.grid(row=0, column=0, padx=5, pady=5)
        self.detail_frame.grid_propagate(False)  # Prevenir que el frame cambie de tamaño
        
        self.detail_label = ttk.Label(self.detail_frame)
        self.detail_label.pack()
        
        self.video_playing = False
        
    def start_detection(self):
        self.start_button.config(state="disabled")
        self.stop_button.config(state="enabled")
        self.video_playing = True
        self.cap = cv2.VideoCapture(0)
        self.update()
        
    def stop_detection(self):
        self.start_button.config(state="enabled")
        self.stop_button.config(state="disabled")
        self.video_playing = False
        self.cap.release()
        self.realtime_label.configure(image=None)
        self.detail_label.configure(image=None)
        
    def update(self):
        ret, frame = self.cap.read()
        if ret and self.video_playing:
            result = self.model.predict(frame, imgsz=640, conf=0.75)
            print(f"Resultados: {result}")

            # Mapear clases a número de dedos
            class_labels = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}

            # Extraer las clases de los resultados
            boxes = result[0].boxes
            classes_detected = boxes.cls.tolist() if boxes is not None else []

            # Calcular el número total de dedos detectados
            num_dedos = sum([class_labels[cls] for cls in classes_detected if cls in class_labels])

            # Contar el número de clases detectadas
            clases_detectadas = len(set(classes_detected))

            # Contar el número de manos detectadas
            num_manos = sum([1 for cls in classes_detected if cls in class_labels])

            # Calcular la frecuencia de cada clase
            # frecuencia_clases = {cls: classes_detected.count(cls) for cls in set(classes_detected)}

            # Calcular el área promedio de detección
            areas = [(box[2] - box[0]) * (box[3] - box[1]) for box in boxes.xyxy] if boxes is not None else []
            area_promedio = sum(areas) / len(areas) if areas else 0

            # Calcular la confianza promedio
            confidences = boxes.conf.tolist() if boxes is not None else []
            confianza_promedio = sum(confidences) / len(confidences) if confidences else 0

            # Obtener la velocidad de procesamiento
            # velocidad_procesamiento = result[0].speed['inference']

            # Contar el número de manos con cada clase específica
            manos_clase_1 = classes_detected.count(0)
            manos_clase_2 = classes_detected.count(1)
            manos_clase_3 = classes_detected.count(2)
            manos_clase_4 = classes_detected.count(3)
            manos_clase_5 = classes_detected.count(4)

            # Actualizar los labels con los resultados
            self.dedos_label.config(text=f"Dedos detectados: {num_dedos}")
            self.clases_label.config(text=f"Clases detectadas: {clases_detectadas}")
            self.manos_label.config(text=f"Manos detectadas: {num_manos}")
            self.area_promedio_label.config(text=f"Área promedio: {area_promedio:.2f}")
            self.confianza_promedio_label.config(text=f"Confianza promedio: {confianza_promedio:.2f}")
            self.manos_clase_1_label.config(text=f"Manos con clase 1: {manos_clase_1}")
            self.manos_clase_2_label.config(text=f"Manos con clase 2: {manos_clase_2}")
            self.manos_clase_3_label.config(text=f"Manos con clase 3: {manos_clase_3}")
            self.manos_clase_4_label.config(text=f"Manos con clase 4: {manos_clase_4}")
            self.manos_clase_5_label.config(text=f"Manos con clase 5: {manos_clase_5}")

            annotated_frame = result[0].plot()
            self.display_image(annotated_frame, self.realtime_label)
            self.display_image(frame, self.detail_label)
            self.root.after(10, self.update)
        else:
            self.stop_detection()
        
    def display_image(self, frame, label_widget):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        label_widget.img = img
        label_widget.configure(image=img)

if __name__ == "__main__":
    root = tk.Tk()
    app = YOLOInterface(root)
    root.mainloop()

