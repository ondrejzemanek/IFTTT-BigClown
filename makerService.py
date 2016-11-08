from urllib.parse import urlencode
from urllib.request import Request, urlopen


class MakerServiceSender:
    """IFTTT Maker service comunication class"""

    _url_prefix = 'https://maker.ifttt.com/trigger/'
    _key_prefix = '/with/key/'
    _recipe_name = None
    _key = None

    def __init__(self, recipe_name, key):
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
