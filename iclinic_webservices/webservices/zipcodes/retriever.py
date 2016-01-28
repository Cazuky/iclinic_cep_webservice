from .models import ZipCode
from .exceptions import InvalidZipCodeFormatException, PostmonZipCodeNotFound
from django.conf import settings

import requests
import json
import re


class ZipCodeRetriever(object):

    def __init__(self, zip_code):
        if self.validate_zip_code_format(zip_code):
            self.zip_code = zip_code
        else:
            raise InvalidZipCodeFormatException

    def fetch(self):
        url = settings.POSTMON_API_URL % { 'cep': self.zip_code }
        response = requests.get(url)

        if response.status_code == 404:
            raise PostmonZipCodeNotFound

        if response.status_code == 200:
            return json.loads(response.text)

        return response.status_code, response.text

    def validate_zip_code_format(self, zip_code):
        match = re.match(r'^\d{5}\-\d{3}$', zip_code)
        if match:
            return True
        return False

