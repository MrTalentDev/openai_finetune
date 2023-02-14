import paho.mqtt.client as mqtt
from django.conf import settings
from .scrap_ft import main
from users.models import User
from .models import FineTunedModels
import json
import time
import concurrent.futures
from threading import Thread
from .mqtt_2 import client as mqtt_2_client

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag=True #set flag
        print('Connected successfully')
        mqtt_client.subscribe("django/request/setting")
    else:
        print('Bad connection. Code:', rc)

def on_disconnect(mqtt_client, userdata, rc):
    print('disconnected',rc)

def newPublish(doc, user):
    # try:
    model_id = main(doc,user)
    data = {"code": 200, "message": "success", "body": model_id}
    # except Exception as e: 
        # data = {"code": 500, "message": "error", "body": "openai error"}

    print(f'____________Web scrapping and Fine-Tuning is ended_______________')
    # model_id='asdfs'
    # delay =600
    # i = 0
    # while i < delay :
    #     print(i)
    #     time.sleep(20)
    #     i+=20
    
    # 4 send model_id
    while True:
        if mqtt_2_client.is_connected:
            rc, mid = mqtt_2_client.publish('django/response/setting/freefox0101@outlook.com', json.dumps(data))
            print('rc',rc, 'mid', mid)
            # i+=1
            break
        else:
            time.sleep(1)
            mqtt_2_client.reconnect()
    # i=0
    print(f'____________________Send Fine-Tuned Model Id_____________________')
    
    User.objects.filter(email=user).update(is_loading=False, loading_doc='')
def on_message(mqtt_client, userdata, msg):
    #1 receive request to update setting\
    payload = json.loads(msg.payload)
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    print(f'____________________Received Update Request______________________')

    # 2 send response to update request
    usr = User.objects.filter(email=payload['user']).get()
    print('usr', usr.is_loading)
    if usr.is_loading:
        resp = json.dumps({
            'message': 'error',
            'body': 'Now, server is fine-tuning your data'
        })
    else:
        resp = json.dumps({
            'message': 'success',
            'body': 'Congratlation, Fine-Tuning started'
        })
    print('resp', resp)
    User.objects.filter(email=payload['user']).update(is_loading=True, loading_doc=payload['doc_url'])

    rc, mid = mqtt_client.publish("django/response/setting/"+payload['user'], resp)
    print('111rc',rc, 'mid', mid)
    print(f'________________Send Respond to Update Request___________________')

    #3 start to scrape and fine-tune
    # https://colleendlgd.wixsite.com/colleendelgado

    # print('rc',payload['doc_url'], 'mid', payload['user'])
    # model_id = main(payload['doc_url'], payload['user'])
    background_thread = Thread(target=newPublish, args=(payload['doc_url'],payload['user']))
    background_thread.start()
    # rc, mid = mqtt_2_client.publish('django/response/setting/freefox0101@outlook.com', json.dumps(resp))
    # print('rc',rc, 'mid', mid)
    # delay = 200
    # i = 0
    # while i < delay :
    #     print(i)
    #     time.sleep(20)
    #     i+=20
    
    # print(i)

client = mqtt.Client()
client.connected_flag=False#create flag in class
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.loop_start()
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE,
)

while not client.connected_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)