import tkinter as tk
import time
import json
from paho.mqtt import client as mqtt

root = tk.Tk()
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_id)

# IP & Port of Thouzer Basic
ip = '192.168.212.1'
port = 1883 

# Username & Password of Thouzer Basic
username = 'SmartRobot'
password = 'SmartRobot'

topic_pub = '0/WHISPERER/RMS-10B1-AAJ65/nav'
topic_pub1 = '0/THOUZER_HW/RMS-10B1-AAJ65/exec/cmd'
address_api = '/home/a/Desktop/voice_pro_max/mqtt_api'

# Connect to MQTT server
def mqtt_connect():
    mqttClient.username_pw_set(username, password)  # MQTT Server PW
    mqttClient.connect(ip, port, 60)
    mqttClient.loop_start()
    # print('Connect Sucessfully')

def start_motion_json():
    with open(address_api + '/start_motion.json', 'r') as read_file :
        api = json.load(read_file)
    return api

def open_json(n):
    if n == 1 :
        with open(address_api + '/moving_forward_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 2 :
        with open(address_api + '/moving_30_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 3 :
        with open(address_api + '/moving_-30_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 4 :
        with open(address_api + '/moving_backward_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file) 
    # elif n == 7 :
    #     with open(address_api + '/MT_MemorizeMode.json', 'r') as read_file :
    #         api = json.load(read_file)
    # elif n == 8 :
    #     with open(address_api + '/pub_MT_700.json', 'r') as read_file :
    #         api = json.load(read_file)
    return api

def on_publish_start():
    msg = str(start_motion_json())
    msg = msg.replace("'",'"')
    # print(msg)
    mqttClient.publish(topic_pub1, f'{msg}')

def on_publish(n):
    msg = str(open_json(n))
    msg = msg.replace("'",'"')
    # print(msg)
    mqttClient.publish(topic_pub, f'{msg}')
    # mqttClient.publish(topic_pub1, f'{msg}')

def on_publish1(n):
    msg = str(open_json(n))
    msg = msg.replace("'",'"')
    # print(msg)
    mqttClient.publish(topic_pub1, f'{msg}')

params = {}
def on_message_come(client, userdata, msg):       
    global params
    _str = str(msg.payload.decode('gb2312'))
    params = json.loads(_str)
    # print('Topic: ' + msg.topic + ', Message: ' + str(msg.payload.decode('gb2312')))

if __name__ == '__main__':
    mqtt_connect()
    on_publish_start()
    while True :
        n = int(input())
        if n<=4:
            mqtt_connect()
            on_publish(n)
        elif n>4:
            on_publish1(n)
        else :
            break
root.mainloop()


