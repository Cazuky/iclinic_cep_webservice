"""
    api.py
    This is the module that handle the API calls
"""
import logging

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.exceptions import BadRequest, NotFound

from django.db import IntegrityError
from django.conf import settings

from iclinic_webservices.webservices.zipcodes.models import ZipCode
from iclinic_webservices.webservices.apikeys.models import ApiKey
from iclinic_webservices.webservices.zipcodes.retriever import ZipCodeRetriever

from iclinic_webservices.webservices.zipcodes.exceptions import \
    InvalidZipCodeFormatException, PostmonZipCodeNotFound


logger = logging.getLogger(__name__)


class ZipCodeResource(DjangoResource):
    """
        This is the ZipCode API
    """
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
            return api_key.active
        except ApiKey.DoesNotExist:
            return False

    def list(self):
        limit = self.request.GET.get('limit')
        logger.info('[API LIST] List zipcodes limit=%s', limit)
        zip_codes = ZipCode.objects.all()

        if limit:
            return zip_codes[:limit]

        return zip_codes

    def create(self):
        zip_code = self.data.get('zip_code')

        logger.info('[API CREATE] Create zipcode. zip_code=%s', zip_code)

        try:
            retriever = ZipCodeRetriever(zip_code)
        except InvalidZipCodeFormatException:
            error = "Invalid %s zip code format." % zip_code
            logger.error('[API CREATE] Error on create zipcode. '
                         'zip_code=%s error=%s', zip_code, error)

            raise BadRequest(error)

        try:
            data = retriever.fetch()
            logger.info('[API CREATE] Create zipcode. zip_code=%s data=%s',
                        zip_code, data)

            zip_code_data = {
                'city': data.get('cidade'),
                'state': data.get('estado'),
                'zip_code': data.get('cep'),
                'address': data.get('logradouro'),
                'neighborhood': data.get('bairro')
            }

            try:
                zip_code_object = ZipCode.objects.create(**zip_code_data)
                logger.info('[API CREATE] Zipcode created. zip_code=%s', zip_code)
                return zip_code_object
            except IntegrityError as exception:
                error_message = exception[1]
                logger.error('[API CREATE] Error on create zipcode. '
                             'zip_code=%s error=%s', zip_code, error_message)

                raise BadRequest(error_message)
        except PostmonZipCodeNotFound:
            error = "Zipcode %s not found in Postmon." % zip_code
            logger.error('[API CREATE] Error on create zipcode. '
                         'zip_code=%s error=%s', zip_code, error)

            raise BadRequest(error)

    def detail(self, zip_code):
        logger.info('[API DETAIL] Get zipcode details. zip_code=%s', zip_code)
        try:
            zip_code_object = ZipCode.objects.get(zip_code=zip_code)
        except ZipCode.DoesNotExist:
            error = "Zipcode %s not found in the database." % zip_code
            logger.info('[API DETAIL] Error on getting zipcode details. '
                        'zip_code=%s error=%s', zip_code, error)
            raise NotFound(error)

        return zip_code_object

    def delete(self, zip_code):
        logger.info('[API DELETE] Delete zipcode. zip_code=%s', zip_code)
        try:
            zip_code_object = ZipCode.objects.get(zip_code=zip_code)
        except ZipCode.DoesNotExist:
            error = "Zipcode %s not found in the database." % zip_code
            logger.info('[API DELETE] Error on deleting zipcode details. '
                        'zip_code=%s error=%s', zip_code, error)
            raise NotFound(error)

        zip_code_object.delete()
