import random
import string
import hashlib

import factory
from factory.django import DjangoModelFactory

from iclinic_webservices.webservices.zipcodes.models import ZipCode
from iclinic_webservices.webservices.apikeys.models import ApiKey


def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for x in xrange(length))


def generate_md5():
    md5 = hashlib.md5()
    return md5.hexdigest()


class ZipCodeFactory(DjangoModelFactory):
    class Meta:
        model = ZipCode

    city = factory.Faker('city', locale='pt_BR')
    state = factory.Faker('estado_sigla', locale='pt_BR')
    address = factory.Faker('street_address', locale='pt_BR')
    zip_code = factory.Faker('postcode', locale='pt_BR')
    neighborhood = factory.Faker('bairro', locale='pt_BR')


class ApiKeyFactory(DjangoModelFactory):
    class Meta:
        model = ApiKey

    key = factory.LazyAttribute(lambda t: generate_md5())
    active = factory.LazyAttribute(lambda t: True)
