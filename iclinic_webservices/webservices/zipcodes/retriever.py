from .models import ZipCode
from .exceptions import InvalidZipCodeFormatException, PostmonZipCodeNotFound
from django.conf import settings

import requests
import json
import re


class ZipCodeRetriever(object):
    """
    This class has the responsability to talk to the Postmon API
    """

    def __init__(self, zip_code):
        if self.validate_zip_code_format(zip_code):
            self.zip_code = zip_code
        else:
            raise InvalidZipCodeFormatException

    def fetch(self):
        """
        This method run a GET http request to the Postmon API
        and returns the information about the zip_code, if exists.

        Result Example:
         {u'bairro': u'Jardim Am\xe9rica',
              u'cep': u'14020260',
              u'cidade': u'Ribeir\xe3o Preto',
              u'cidade_info': {u'area_km2': u'650,955', u'codigo_ibge': u'3543402'},
              u'complemento': u'at\xe9 489 - lado \xedmpar',
              u'estado': u'SP',
              u'estado_info': {u'area_km2': u'248.222,362',
               u'codigo_ibge': u'35',
               u'nome': u'S\xe3o Paulo'},
          u'logradouro': u'Avenida Presidente Vargas'})
        """
        url = settings.POSTMON_API_URL % {'cep': self.zip_code}
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

