import umqtt.robust as umqtt
from network import WLAN
import time

from machine import Pin, Timer

import schema_upb2 as pb


HOSTNAME = '10.94.123.254'
PORT = 5050
TOPIC = 'temp/pico'

wifi = WLAN(WLAN.IF_STA)
wifi.active(True)

ssid = ''
password = ''

mqtt = umqtt.MQTTClient(
    client_id = b'subscriber',
    server = HOSTNAME.encode(),
    port = PORT,
    keepalive = 7000
)


def connect(
    wifi_obj,
    ssid,
    password,
    timeout =10
):
    wifi_obj.connect(ssid,password)
    
    while timeout > 0:
        if wifi_obj.status() !=3:
            time.sleep(1)
            timeout -= 1
        else:
            return True
        
    return False

wifi.connect(ssid,password)
time.sleep(2)

if wifi.status() != 3:
    print("Could not connect")
else:
    print("Sucessfully connected")
    
def decode_message(data):
    message = pb.TempReading()
    result = message.decode(data)
    return result if result is not None else message


def callback(topic,message):
    message = pb.TempReading.decode(message)
    
    t = message.time
    
    print('[%02d: %02d: %02d] %s: temperature is %.2f' % ( t.hour, t.minute, t.seconds, message.publisher_id, message.temperature))
    #temp = float(message)
    
    led = Pin("LED", Pin.OUT)
    
    if message.temperature > 30 :
        led.on()
        
    else :
        led.off()

mqtt.connect()

mqtt.set_callback(callback)
mqtt.subscribe(TOPIC)

while True:
    mqtt.
    wait_msg()



