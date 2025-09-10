import paho.mqtt.client as mqtt
import time

# Configuración del broker MQTT
broker = "8468378e2c4c42ddabd1eb1524b0629a.s1.eu.hivemq.cloud"
port = 8883  # Puerto seguro para TLS
topic = "casa/accion"  # Tema en el que publicará
message = "Encender"  # Mensaje a enviar

# Callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado correctamente al broker")
    else:
        print("Error de conexión, código: ", rc)

# Crear una instancia del cliente MQTT
client = mqtt.Client()

# Configuración para TLS/SSL
client.tls_set()  # Configura TLS por defecto

# Asignar el callback de conexión
client.on_connect = on_connect

# Conectar al broker
client.connect(broker, port)

# Publicar un mensaje
client.publish(topic, message)

# Iniciar el bucle del cliente para enviar y recibir datos
client.loop_start()

# Esperar unos segundos para asegurar que el mensaje se envíe antes de terminar el programa
time.sleep(2)

# Detener el bucle y desconectar
client.loop_stop()
client.disconnect()
