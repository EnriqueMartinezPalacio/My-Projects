import os

# Ruta de la carpeta donde están los archivos
carpeta = 'C:/Users/enri-/Desktop/Tesis/Fotos/segundo_Aumentada/'

# Recorremos los archivos en la carpeta
for archivo in os.listdir(carpeta):
    # Verificamos si el archivo es de tipo json, jpg o png
    if archivo.endswith(('.json', '.jpg', '.png')):
        # Si el nombre contiene 'segundo', lo reemplazamos por 'Segundo'
        if 'segundo' in archivo.lower():  # Usamos .lower() para hacerlo sin importar mayúsculas/minúsculas
            nuevo_nombre = archivo.lower().replace('segundo', 'Segundo')
            ruta_antigua = os.path.join(carpeta, archivo)
            ruta_nueva = os.path.join(carpeta, nuevo_nombre)
            
            # Renombramos el archivo
            os.rename(ruta_antigua, ruta_nueva)
            print(f"Renombrado: {archivo} -> {nuevo_nombre}")
