from iclinic_webservices.settings.base import *


INSTALLED_APPS += ('iclinic_webservices.webservices.zipcodes', )

POSTMON_API_URL = 'http://api.postmon.com.br/v1/cep/%(cep)s'
