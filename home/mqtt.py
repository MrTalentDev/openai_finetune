import paho.mqtt.client as mqtt
from django.conf import settings
from .scrap_ft import main
from users.models import User
from .models import FineTunedModels
import json
import time
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
    time.sleep(1)
    start_time = time.time()
    finetuned = main(doc,user)
    # print("#####################",finetuned) 
    print("--- %s seconds ---" % (time.time() - start_time))
    # if finetuned.get('code') == 200:
    #     try:
    #         # print("#####################",finetuned.model_id) 
    #         # print("#####################",finetuned.get('model_id')) 
    #         FineTunedModels.objects.get(user_email=user)
    #         FineTunedModels.objects.filter(user_email=user).update(model_id=finetuned.get('body'))
    #     except FineTunedModels.DoesNotExist:
    #         usr = FineTunedModels(user_email=user, model_id=finetuned.get('body')) # create new model instance
    #         usr.save()
    #     except Exception as e:
    #         print(e)
    #     data = {"code": 200, "message": "success", "body": finetuned.get('body')}
    # elif finetuned.get('code') == 500:
    #     data = {"code": 500, "message": "error", "body": finetuned.get('body')}
    # else :
    #     data = {"code": 500, "message": "error", "body": "Error"}

    print(f'____________Web scrapping and Fine-Tuning is ended_______________')
    
    # 4 send model_id
    while True:
        if mqtt_2_client.is_connected:
            rc, mid = mqtt_2_client.publish('django/updated/setting/freefox0101@outlook.com', json.dumps(finetuned))
            print('rc',rc, 'mid', mid)
            # i+=1
            break
        else:
            time.sleep(1)
            mqtt_2_client.reconnect()
    print(f'____________________Send Fine-Tuned Model Id_____________________')
    
    rs = User.objects.filter(email=user).update(is_loading=False, loading_doc='')
    print('user table updated', rs)
    
def on_message(mqtt_client, userdata, msg):
    #1 receive request to update setting
    payload = json.loads(msg.payload)
    print("============================================================")
    print(payload)
    print("============================================================")
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    print(f'____________________Received Update Request______________________')

    # 2 send response to update request
    usr = User.objects.filter(email=payload['user']).get()
    # print('usr', usr.is_loading)
    if usr.is_loading:
        resp = json.dumps({
            'code': '500',
            'message': 'error',
            'body': 'Now, server is fine-tuning on '+usr.loading_doc
        })
    else:
        resp = json.dumps({
            'code': '200',
            'message': 'success',
            'body': 'Congratulation, Fine-Tuning started'
        })
        
        background_thread = Thread(target=newPublish, args=(payload['doc_url'],payload['user']))
        background_thread.start()
        
        # User.objects.filter(email=payload['user']).update(is_loading=True, loading_doc=payload['doc_url'])
    # print('resp', resp)

    rc, mid = mqtt_client.publish("django/response/setting/"+payload['user'], resp)
    print('response ', 'rc', rc, 'mid', mid)
    print(f'________________Send Respond to Update Request___________________')

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