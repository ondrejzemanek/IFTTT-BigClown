#!/usr/bin/env python3

from urllib.parse import urlencode
from urllib.request import Request, urlopen

#IFTTT Maker channel comunication class
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

