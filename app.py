from flask import Flask
from flasgger import Swagger
import paho.mqtt.client as mqtt

# Inicializar Flask y Swagger
app = Flask(__name__)
swagger = Swagger(app)

# Configuración de MQTT
MQTT_BROKER = "broker.hivemq.com"  # Broker público de ejemplo
MQTT_PORT = 1883
MQTT_TOPIC = "hola/mundo"

# Función de conexión con MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker con código de resultado: " + str(rc))
    client.subscribe(MQTT_TOPIC)

# Función para manejar los mensajes recibidos
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en el tema {msg.topic}: {msg.payload.decode()}")

# Configuración del cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Rutas de Flask
@app.route('/hello', methods=['GET'])
def hello_world():
    """
    Esta ruta devuelve un mensaje de saludo
    ---
    responses:
      200:
        description: Saludo
        examples:
          application/json: {'message': 'Hola Mundo desde MQTT!'}
    """
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()  # Empezar el bucle MQTT
    mqtt_client.publish(MQTT_TOPIC, "¡Hola Mundo desde MQTT!")
    return {"message": "Hola Mundo desde MQTT!"}

if __name__ == '__main__':
    app.run(debug=True)
