from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from iclinic_webservices.webservices.zipcodes.models import ZipCode
from iclinic_webservices.webservices.apikeys.models import ApiKey


class ZipCodeResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'city': 'city',
        'state': 'state',
        'addreess': 'address',
        'zip_code': 'zip_code',
        'neighborhood': 'neighborhood'
    })

    def is_authenticated(self):
        try:
            api_key = ApiKey.objects.get(key=self.request.GET.get('api_key'))
            if api_key.active:
                return True
            else:
                return False
        except ApiKey.DoesNotExist:
            return False

    def list(self):
        return ZipCode.objects.all()

