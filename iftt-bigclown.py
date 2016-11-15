#!/usr/bin/env python3

import json
import requests
import paho.mqtt.client
import threading


class IFTTTWorker(threading.Thread):

    _url = 'https://maker.ifttt.com/trigger/{your_maker_event_name}/with/key/{your_maker_key}'
    _value = None

    def __init__(self, value):
        self._value = value
        threading.Thread.__init__(self)

    def run(self):
        json_data = {'value1': self._value, 'value2': '', 'value3': ''}
        requests.post(self._url, json_data)


if __name__ == '__main__':

    TEMPERATURE_TRESHOLD_HIGH = 21
    TEMPERATURE_TRESHOLD_LOW = 15
    TEMPERATURE_ALARM_HYSTERESIS = 1

    is_temperature_alarm_high = False
    is_temperature_alarm_low = False

    def on_connect(client, userdata, flags, rc):
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
                        IFTTTWorker('Temperature is too high!').start()
                else:
                    if temperature < (TEMPERATURE_TRESHOLD_HIGH - TEMPERATURE_ALARM_HYSTERESIS):
                        is_temperature_alarm_high = False
                        IFTTTWorker('Temperature alarm deactivated').start()

                if not is_temperature_alarm_low:
                    if temperature <= TEMPERATURE_TRESHOLD_LOW:
                        is_temperature_alarm_low = True
                        IFTTTWorker('Temperature is too low!').start()
                else:
                    if temperature > (TEMPERATURE_TRESHOLD_LOW + TEMPERATURE_ALARM_HYSTERESIS):
                        is_temperature_alarm_low = False
                        IFTTTWorker('Temperature alarm deactivated').start()


    client = paho.mqtt.client.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect('localhost')

    client.loop_forever()
