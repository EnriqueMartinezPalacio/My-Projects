import paho.mqtt.client as mqtt

broker_address = "broker.emqx.io"
broker_port = 8883
topic_base = "domotica/"

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
client.connect(broker_address, broker_port)

# Función para publicar un mensaje a un tópico
def publicar_orden(topic, mensaje):
    full_topic = topic_base + topic
    client.publish(topic, mensaje)
    print(f"Mensaje '{mensaje}' enviado al tópico {topic}")

# Iniciar el loop para procesar callbacks y mensajes
client.loop_start()

# Ejemplo: enviar mensaje al tópico de la cocina
publicar_orden("COCINA", "LuzOn")

# Detener el loop y desconectar del broker
client.loop_stop()
client.disconnect()
