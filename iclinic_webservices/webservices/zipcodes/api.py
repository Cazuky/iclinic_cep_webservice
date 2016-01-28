from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from iclinic_webservices.webservices.zipcodes.models import ZipCode


class ZipCodeResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'city': 'city',
        'state': 'state',
        'addreess': 'address',
        'zip_code': 'zip_code',
        'neighborhood': 'neighborhood'
    })


    def list(self):
        return ZipCode.objects.all()

