from django.test import TestCase, Client

from .factories import ZipCodeFactory, ApiKeyFactory


class ZipCodeResourceTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.api_key = ApiKeyFactory.create()

    def test_list(self):
        zip_code = ZipCodeFactory.create()
        url = "/zipcodes/?api_key={0}".format(self.api_key)
        response = self.client.get(url)

        expected = '{"objects": [%s]}' % zip_code.jsonify()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected)
