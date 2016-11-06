#!/usr/bin/env python3

# #Simple temperature control class
class TemperatureControl:

    __treshold = 20
    __actTreshold = 20

    def __init__(self, treshold):
        self.treshold = treshold
        self.actTreshold = treshold

    def HighTemperature(self, value):
        ''':param value: actual temperature
        :return: Return true if actual temperature is higher than threshold.'''
        value = round(value)
        if value > self.actTreshold:
            self.actTreshold = value
            return True
        elif value - 5 < self.actTreshold and value > self.treshold:
            self.actTreshold = value

        return False

    def LowTemperature(self, value):
        ''':param value: actual temperature
        :return: Return true if actual temperature is lower than threshold.'''
        value = round(value)
        if value < self.actTreshold:
            return True
            self.actTreshold = value
        elif value - 5 > self.actTreshold and value < self.treshold:
            self.actTreshold = value

        return False