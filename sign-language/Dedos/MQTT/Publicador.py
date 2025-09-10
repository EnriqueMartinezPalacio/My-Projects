import paho.mqtt.client as mqtt

# Configuración del broker MQTT
broker = "broker.emqx.io"
port = 8883  # Puerto TLS
topic = "Salida_01"



# Función que se llama cuando el cliente se conecta al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
    else:
        print(f"Conexión fallida, código de error {rc}")

# Crear una instancia del cliente MQTT
client = mqtt.Client()



# Configurar la conexión TLS
client.tls_set()  # Usar TLS sin verificación de certificados (para pruebas)
client.on_connect = on_connect

# Conectar al broker
client.connect(broker, port)

# Publicar mensajes
client.loop_start()  # Iniciar el loop para procesar callbacks y mensajes
client.publish(topic, "Encender")
print(f"Mensaje 'Encender' enviado al tema '{topic}'")
client.publish(topic, "Apagar")
print(f"Mensaje 'Apagar' enviado al tema '{topic}'")

client.loop_stop()  # Detener el loop
client.disconnect()  # Desconectar del broker
