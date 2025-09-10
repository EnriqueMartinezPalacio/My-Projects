import queue
import threading
import tkinter as tk
import time

# ======================== Interfaz gráfica (Tkinter) ======================== #
# Función para actualizar la ventana con la frase final
def actualizar_frase_final(frase, topico, mensaje, tiempo_formateado):
    frase_label.config(text=f"Frase Final: {frase}")
    topico_label.config(text=f"Tópico: {topico}")
    mensaje_label.config(text=f"Mensaje: {mensaje}")
    tiempo_label.config(text=f"Tiempo: {tiempo_formateado}")
    root.update_idletasks()

# Inicializar la ventana de tkinter
root = tk.Tk()
root.title("Frase Final")
root.geometry("400x200")

# Crear etiquetas para la ventana
frase_label = tk.Label(root, text="Frase Final: ", font=("Arial", 16))
frase_label.pack(pady=20)
topico_label = tk.Label(root, text="Tópico: ", font=("Arial", 12))
topico_label.pack(pady=5)
mensaje_label = tk.Label(root, text="Mensaje: ", font=("Arial", 12))
mensaje_label.pack(pady=5)
tiempo_label = tk.Label(root, text="Tiempo: ", font=("Arial", 12))
tiempo_label.pack(pady=5)

# ======================== Lógica del temporizador ======================== #
# Cola para manejar la comunicación entre hilos
tiempo_queue = queue.Queue()

def temporizador(duracion):
    tiempo_restante = duracion
    while tiempo_restante > 0:
        minutos = tiempo_restante // 60  # Calcula los minutos
        segundos = tiempo_restante % 60  # Calcula los segundos restantes
        tiempo_formateado = f"{minutos:02d}:{segundos:02d}"  # Formato MM:SS
        tiempo_queue.put(tiempo_formateado)  # Enviar el tiempo formateado a la cola
        time.sleep(1)
        tiempo_restante -= 1
    tiempo_queue.put("00:00")  # Al finalizar, poner "00:00"

def iniciar_temporizador(duracion):
    # Inicia el hilo del temporizador
    thread = threading.Thread(target=temporizador, args=(duracion,))
    thread.start()

def actualizar_tiempo():
    try:
        # Obtener el tiempo formateado desde la cola si está disponible
        while not tiempo_queue.empty():
            tiempo_formateado = tiempo_queue.get_nowait()
            tiempo_label.config(text=f"Tiempo: {tiempo_formateado}")
        
        # Llamar a esta función después de 100 ms para seguir actualizando
        root.after(100, actualizar_tiempo)

    except queue.Empty:
        pass

# Iniciar la actualización del tiempo en la interfaz
root.after(100, actualizar_tiempo)

# Para fines de prueba: Iniciar temporizador de 5 segundos
iniciar_temporizador(5)

# Ejecutar el bucle principal de la interfaz
root.mainloop()
