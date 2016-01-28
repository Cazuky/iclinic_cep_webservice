from django.test import TestCase
from iclinic_webservices.webservices.zipcodes.retriever import ZipCodeRetriever
from iclinic_webservices.webservices.zipcodes.exceptions import InvalidZipCodeFormatException, PostmonZipCodeNotFound


class ZipCodeRetrieverTestCase(TestCase):

    def setUp(self):
        self.zip_code = '14020-260'
        self.zip_code_invalid = '1402-260'
        self.zip_code_inexistent = '33333-333'

    def test_zip_code_invalid_format(self):
        zip_code = self.zip_code_invalid

        with self.assertRaises(InvalidZipCodeFormatException):
            ZipCodeRetriever(zip_code)

    def test_zip_code_not_found(self):
        zip_code = self.zip_code_inexistent
        retriever = ZipCodeRetriever(zip_code)

        with self.assertRaises(PostmonZipCodeNotFound):
            retriever.fetch()

    def test_fetch(self):
        zip_code = self.zip_code
        retriever = ZipCodeRetriever(zip_code)
        result = retriever.fetch()

        self.assertIsInstance(result, dict)
        self.assertIn('cep', result.keys())
