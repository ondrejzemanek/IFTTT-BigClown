#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class MakerChannelSender:

    url_prefix = 'https://maker.ifttt.com/trigger/'
    key_prefix = '/with/key/'

    recipe_name = None
    key = None

    def __init__(self, recipe_name, key):
        self.recipe_name = recipe_name
        self.key = key

    def __create_url__(self):
        if self.recipe_name is None or self.key is None:
            return None
        else:
            return self.url_prefix + self.recipe_name + self.key_prefix + self.key

    def make_request(self, value1, value2, value3):
        url = self.__create_url__()

        if url is not None:
            post_fields = {"value1": value1, "value2": value2, "value3": value3}
            request = Request(url, urlencode(post_fields).encode())
            return urlopen(request).read().decode()
        else:
            return None

    def receive_request(self):
        url = self.__create_url__()

        if url is not None:
            request = Request(url)
            return urlopen(request).read().decode()
        else:
            return None

maker = MakerChannelSender('high_temperature', 'iClY1--OeGUNreTpASC7Dl42mWgjFcc19eHSWLGaAjA')

prefix = 'nodes/bridge/0/'

table = {
    "led/-" : {"state" : {"pin" : '1'}},
    "thermometer/i2c0-48" : {"temperature" : {"pin" : '2'}},
    "thermometer/i2c1-48" : {"temperature" : {"pin" : '3'}},
    "thermometer/i2c0-49" : {"temperature" : {"pin" : '4'}},
    "thermometer/i2c1-49" : {"temperature" : {"pin" : '5'}},
    "lux-meter/i2c0-44" : {"illuminance" : {"pin" : '6'}},
    "lux-meter/i2c1-44" : {"illuminance" : {"pin" : '7'}},
    "lux-meter/i2c0-45" : {"illuminance" : {"pin" : '8'}},
    "lux-meter/i2c1-45" : {"illuminance" : {"pin" : '9'}},
    "barometer/i2c0-60" : {"pressure," : {"pin" : '10'}, "altitude" : {"pin" : '11'}},
    "barometer/i2c1-60" : {"pressure," : {"pin" : '12'}, "altitude" : {"pin" : '13'}},
    "humidity-sensor/i2c0-5f" : {"relative-humidity" : {"pin" : '14'}, "temperature" : {"pin" : '15'}},
    "humidity-sensor/i2c1-5f" : {"relative-humidity" : {"pin" : '16'}, "temperature" : {"pin" : '17'}},
    "co2-sensor/i2c0-38" : {"concentration" : {"pin" : '18'}},
    "relay/i2c0-3b" : {"state" : {"pin" : '19'}},
    "relay/i2c0-3f" : {"state" : {"pin" : '20'}}
}

def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(prefix + "#")


def on_message(client, userdata, msg):
    sensor = table.get(msg.topic[len(prefix):], None)

    if sensor:
        payload = json.loads(msg.payload.decode('utf-8'))

        for k, v in payload.items():
            if isinstance(v, bool) or v is None:
                print(str(k) + ": " + str(v))
            elif isinstance(v, list):
                for d in v:
                    print(str(k) + ": " + str(d))
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #maker.make_request(value, None, None) #send data to IFTTT Maker
        #print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.24", 1883, 60)

client.loop_forever()

