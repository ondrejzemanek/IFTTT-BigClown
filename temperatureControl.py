class TemperatureControl:
    """Simple temperature control class"""

    _max_temperature = 20

    def __init__(self):
        self._max_temperature = 20

    def is_higher(self, value):
        """ :param value: actual temperature
            :return: Return true if actual temperature is higher than max_temperature.
        """
        value = round(value)
        if value > self._max_temperature:
            self._max_temperature = value
            return True
        else:
            return False
