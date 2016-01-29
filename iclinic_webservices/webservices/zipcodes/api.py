import logging

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.exceptions import BadRequest, NotFound

from django.db import IntegrityError
from django.conf import settings

from iclinic_webservices.webservices.zipcodes.models import ZipCode
from iclinic_webservices.webservices.apikeys.models import ApiKey
from iclinic_webservices.webservices.zipcodes.retriever import ZipCodeRetriever

from iclinic_webservices.webservices.zipcodes.exceptions import InvalidZipCodeFormatException, PostmonZipCodeNotFound


logger = logging.getLogger(__name__)


class ZipCodeResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'city': 'city',
        'state': 'state',
        'address': 'address',
        'zip_code': 'zip_code',
        'neighborhood': 'neighborhood'
    })

    def is_debug(self):
        return settings.DEBUG

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
        logger.info('[API LIST] List zipcodes')
        return ZipCode.objects.all()

    def create(self):
        logger.info('[API CREATE] Create zipcode. zip_code=%s' % self.data.get('zip_code'))
        zip_code = self.data.get('zip_code')

        try:
            retriever = ZipCodeRetriever(zip_code)
            data = retriever.fetch()
            logger.info('[API CREATE] Create zipcode. zip_code=%s data=%s' % (zip_code, data))
        except InvalidZipCodeFormatException:
            error = "Invalid %s zip code format." % zip_code
            logger.error('[API CREATE] Error on create zipcode. zip_code=%s error=%s' % (zip_code, error))

            raise BadRequest(error)

        except PostmonZipCodeNotFound:
            error = "Zipcode %s not found in Postmon." % zip_code
            logger.error('[API CREATE] Error on create zipcode. zip_code=%s error=%s' % (zip_code, error))

            raise BadRequest(error)

        zip_code_data = {
            'city': data.get('cidade'),
            'state': data.get('estado'),
            'zip_code': data.get('cep'),
            'address': data.get('logradouro'),
            'neighborhood': data.get('bairro')
        }

        try:
            zip_code_object = ZipCode.objects.create(**zip_code_data)

            logger.info('[API CREATE] Zipcode created. zip_code=%s' % zip_code)

            return zip_code_object
        except IntegrityError as e:
            error_code, error_message = e
            logger.error('[API CREATE] Error on create zipcode. zip_code=%s error=%s' % (zip_code, error_message))

            raise BadRequest(error_message)

    def detail(self, zip_code):
        logger.info('[API DETAIL] Get zipcode details. zip_code=%s' % zip_code)
        try:
            zip_code_object = ZipCode.objects.get(zip_code=zip_code)
        except ZipCode.DoesNotExist:
            error = "Zipcode %s not found in the database." % zip_code
            logger.info("[API DETAIL] Error on getting zipcode details. zip_code=%s error=%s" % (zip_code, error))

            raise NotFound(error)

        return zip_code_object

    def delete(self, zip_code):
        logger.info('[API DELETE] Delete zipcode. zip_code=%s' % zip_code)
        try:
            zip_code_object = ZipCode.objects.get(zip_code=zip_code)
        except ZipCode.DoesNotExist:
            error = "Zipcode %s not found in the database." % zip_code
            logger.info("[API DELETE] Error on deleting zipcode details. zip_code=%s error=%s" % (zip_code, error))

            raise NotFound(error)

        zip_code_object.delete()
