import os
import json

# Define la carpeta donde están los archivos JSON
carpeta = 'C:/Users/enri-/Desktop/Tesis/DataSets/DataSet_Acciones/Hora/'

# Define la etiqueta incorrecta y la correcta
etiqueta_incorrecta = 'segundo'
etiqueta_correcta = 'Segundo'

# Recorre todos los archivos en la carpeta
for archivo in os.listdir(carpeta):
    # Verifica que el archivo sea un archivo JSON
    if archivo.endswith('.json'):
        ruta_archivo = os.path.join(carpeta, archivo)
        
        # Abre y carga el contenido del archivo JSON
        with open(ruta_archivo, 'r') as f:
            datos = json.load(f)
        
        # Recorre las formas y cambia el nombre de la etiqueta
        cambio_realizado = False
        for forma in datos['shapes']:
            if forma['label'] == etiqueta_incorrecta:
                forma['label'] = etiqueta_correcta
                cambio_realizado = True
        
        # Guarda el archivo JSON si se realizó un cambio
        if cambio_realizado:
            with open(ruta_archivo, 'w') as f:
                json.dump(datos, f, indent=4)

print("Cambio de etiquetas completado.")
