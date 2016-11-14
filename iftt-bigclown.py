#!/usr/bin/env python3

import sys
import json
import requests
import paho.mqtt.client
import threading


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
            json_data = {'value1': value1, 'value2': value2, 'value3': value3}
            return requests.post(url, None, json_data)


if __name__ == '__main__':
    # MQTT settings
    HUB_PREFIX = 'nodes/bridge/0/'
    DEV_IP_ADDRESS = '192.168.0.24'
    DEV_PORT = 1883
    KEEP_ALIVE = 60

    # Maker settings
    MAKER_SERVICE_NAME = '{your_maker_event_name}'
    MAKER_SERVICE_KEY = '{your_maker_key}'

    # Temperature control
    TEMPERATURE_TRESHOLD_HIGH = 21
    TEMPERATURE_TRESHOLD_LOW = 15
    TEMPERATURE_ALARM_HYSTERESIS = 1

    is_temperature_alarm_high = False
    is_temperature_alarm_low = False
    lock = threading.Lock()

    def on_connect(client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        client.subscribe(HUB_PREFIX + "#")


    def on_message(client, userdata, msg):
        t = threading.Thread(target=check_temperature, name=None, args=[msg])
        t.start()


    def check_temperature(msg):
        global is_temperature_alarm_high
        global is_temperature_alarm_low
        payload = json.loads(msg.payload.decode('utf-8'))
        for key, value in payload.items():
            if key == 'temperature':
                with lock:
                    temperature = value[0]
                    if not is_temperature_alarm_high:
                        if temperature >= TEMPERATURE_TRESHOLD_HIGH:
                            is_temperature_alarm_high = True
                            maker.make_request("Temperature is too high!", '', '')
                    else:
                        if temperature < (TEMPERATURE_TRESHOLD_HIGH - TEMPERATURE_ALARM_HYSTERESIS):
                            is_temperature_alarm_high = False
                            maker.make_request("Temperature alarm deactivated", '', '')

                    if not is_temperature_alarm_low:
                        if temperature <= TEMPERATURE_TRESHOLD_LOW:
                            is_temperature_alarm_low = True
                            maker.make_request("Temperature is too low!", '', '')
                    else:
                        if temperature > (TEMPERATURE_TRESHOLD_LOW + TEMPERATURE_ALARM_HYSTERESIS):
                            is_temperature_alarm_low = False
                            maker.make_request("Temperature alarm deactivated", '', '')


    client = paho.mqtt.client.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(DEV_IP_ADDRESS, DEV_PORT, KEEP_ALIVE)
    except ConnectionRefusedError:
        print('Connection to ' + DEV_IP_ADDRESS + ' refused!')
        sys.exit(1)
    except:
        print('Connection to ' + DEV_IP_ADDRESS + ' failed.')
        sys.exit(1)

    maker = MakerServiceSender(MAKER_SERVICE_NAME, MAKER_SERVICE_KEY)

    client.loop_forever()
