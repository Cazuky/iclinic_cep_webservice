from iclinic_webservices.settings.base import *


INSTALLED_APPS += ('iclinic_webservices.webservices.zipcodes',
                   'iclinic_webservices.webservices.apikeys')

POSTMON_API_URL = 'http://api.postmon.com.br/v1/cep/%(cep)s'
