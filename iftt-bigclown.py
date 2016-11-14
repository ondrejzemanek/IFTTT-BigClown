#!/usr/bin/env python3

import json
import paho.mqtt.client
from threading import Thread
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class TemperatureControl:
    """Simple temperature control class"""

    _max_temperature = 0
    _min_temperature = 0

    def __init__(self, min_temp,  max_temp):
        """
        :param min_temp: bottom temperature treshold
        :param max_temp: top temperature treshold
        """
        self._max_temperature = min_temp
        self._min_temperature = max_temp

    def is_out_of_range(self, value):
        """ :param value: actual temperature
            :return: Return true if actual temperature is higher than max_temperature. (Measurements with hysteresis 1 ° C.)
        """
        value = round(value)
        if value > self._max_temperature or value < self._min_temperature:
            self._max_temperature = value
            return True
        else:
            return False


class MakerServiceSender:
    """IFTTT Maker service comunication class"""

    _url_prefix = 'https://maker.ifttt.com/trigger/'
    _key_prefix = '/with/key/'
    _recipe_name = None
    _key = None

    def __init__(self, recipe_name, key):
        """
        :param recipe_name: your maker service event name
        :param key: your maker service key
        """
        self._recipe_name = recipe_name
        self._key = key

    def _create_url(self):
        if len(str(self._recipe_name)) > 0 and len(str(self._key)) > 0:
            return self._url_prefix + self._recipe_name + self._key_prefix + self._key

    def make_request(self, value1, value2, value3):
        url = self._create_url()

        if url is not None:
            post_fields = {'value1': value1, 'value2': value2, 'value3': value3}
            request = Request(url, urlencode(post_fields).encode())
            return urlopen(request).read().decode()


if __name__ == '__main__':
    # MQTT settings
    HUB_PREFIX = 'nodes/bridge/0/'
    DEV_IP_ADDRESS = '192.168.0.24'
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
                if tempControl.is_out_of_range(value[0]):
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

    tempControl = TemperatureControl(15, 22)

    maker = MakerServiceSender(MAKER_SERVICE_NAME, MAKER_SERVICE_KEY)

    client.loop_forever()
