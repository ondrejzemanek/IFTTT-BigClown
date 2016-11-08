import json
import paho.mqtt.client
from makerService import MakerServiceSender
from temperatureControl import TemperatureControl
from threading import Thread


# MQTT settings
HUB_PREFIX = 'nodes/bridge/0/'
DEV_IP_ADDRESS = '127.0.0.1'
DEV_PORT = 1883
KEEP_ALIVE = 60

# Maker settings
MAKER_SERVICE_NAME = '{your_maker_event_name}'
MAKER_SERVICE_KEY = '{your_maker_key}'


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(HUB_PREFIX + "#")


def on_message(client, userdata, msg):
    t = Thread(target=check_temperature, name=None, args=[msg])
    t.start()


def check_temperature(msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    for key, value in payload.items():
        if key == 'temperature':
            if tempControl.is_higher(value[0]):
                maker.make_request(''.join(str(e) for e in value), '', '')


client = paho.mqtt.client.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(DEV_IP_ADDRESS, DEV_PORT, KEEP_ALIVE)
except ConnectionRefusedError:
    print('Connection to ' + DEV_IP_ADDRESS + ' refused!')
    exit(1)
except:
    print('Connection to ' + DEV_IP_ADDRESS + ' failed.')
    exit(1)

tempControl = TemperatureControl()

maker = MakerServiceSender(MAKER_SERVICE_NAME, MAKER_SERVICE_KEY)

client.loop_forever()
