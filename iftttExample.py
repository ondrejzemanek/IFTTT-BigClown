#!/usr/bin/env python3

from iftttme import MakerChannelSender
from temperatureControl import TemperatureControl
import paho.mqtt.client as mqtt
import json

hubPrefix = 'nodes/bridge/0/'
ipAddress = '192.168.0.101'
port = 1883
makerChannelName = 'high_temperature'
makerChannelKey = 'iClY1--OeGUNreTpASC7Dl42mWgjFcc19eHSWLGaAjA'
temperatureTreshold = 19


tempControl = TemperatureControl(temperatureTreshold)
maker = MakerChannelSender(makerChannelName, makerChannelKey)


# Hub < --- > PI comunication
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(hubPrefix + "#")


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))

    for k, v in payload.items():
        if k == 'temperature':
            if tempControl.HighTemperature(v[0]):
                maker.make_request(str(v[0]) + str(v[1]), '', '') #send data to IFTTT Maker

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ipAddress, port, 60)

client.loop_forever()