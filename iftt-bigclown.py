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
    _url = None

    def __init__(self, recipe_name, key):
        """
        :param recipe_name: your maker service event name
        :param key: your maker service key
        """
        self._url = self._url_prefix + recipe_name + self._key_prefix + key

    def make_request(self, value):
        if self._url is not None:
            json_data = {'value1': value, 'value2': '', 'value3': ''}
            return requests.post(self._url, None, json_data)


class IFTTTWorker(threading.Thread):
    pass


if __name__ == '__main__':
    # Maker settings
    MAKER_SERVICE_NAME = '{your_maker_event_name}'
    MAKER_SERVICE_KEY = '{your_maker_key}'

    # Temperature control
    TEMPERATURE_TRESHOLD_HIGH = 21
    TEMPERATURE_TRESHOLD_LOW = 15
    TEMPERATURE_ALARM_HYSTERESIS = 1

    is_temperature_alarm_high = False
    is_temperature_alarm_low = False

    def on_connect(client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        client.subscribe('nodes/bridge/0/#')


    def on_message(client, userdata, msg):
        global is_temperature_alarm_high
        global is_temperature_alarm_low
        payload = json.loads(msg.payload.decode('utf-8'))
        for key, value in payload.items():
            if key == 'temperature':
                temperature = value[0]
                if not is_temperature_alarm_high:
                    if temperature >= TEMPERATURE_TRESHOLD_HIGH:
                        is_temperature_alarm_high = True
                        IFTTTWorker(target=maker.make_request, args=['Temperature is too high!']).start()
                else:
                    if temperature < (TEMPERATURE_TRESHOLD_HIGH - TEMPERATURE_ALARM_HYSTERESIS):
                        is_temperature_alarm_high = False
                        IFTTTWorker(target=maker.make_request, args=['Temperature alarm deactivated']).start()

                if not is_temperature_alarm_low:
                    if temperature <= TEMPERATURE_TRESHOLD_LOW:
                        is_temperature_alarm_low = True
                        IFTTTWorker(target=maker.make_request, args=['Temperature is too low!']).start()
                else:
                    if temperature > (TEMPERATURE_TRESHOLD_LOW + TEMPERATURE_ALARM_HYSTERESIS):
                        is_temperature_alarm_low = False
                        IFTTTWorker(target=maker.make_request, args=['Temperature alarm deactivated']).start()


    client = paho.mqtt.client.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect('localhost')

    maker = MakerServiceSender(MAKER_SERVICE_NAME, MAKER_SERVICE_KEY)

    ifttt_worker = IFTTTWorker()

    client.loop_forever()
