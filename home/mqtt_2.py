import paho.mqtt.client as mqtt
from django.conf import settings
import time

def on_disconnect(mqtt_client, userdata, rc):
    print('disconnected',rc)

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully____2')
        mqtt_client.subscribe("django/mqtt/asdf")
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    print(f'________________________________') 

client = mqtt.Client()
client.connected_flag_2=False#create flag in class
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
