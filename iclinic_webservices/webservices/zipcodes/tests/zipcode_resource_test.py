from django.test import TestCase, Client

from .factories import ZipCodeFactory, ApiKeyFactory


class ZipCodeResourceTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.api_key = ApiKeyFactory.create()
        self.url = "/zipcodes/?api_key=%s" % self.api_key
        self.url_with_zip_code = "/zipcodes/%(zip_code)s/?api_key=%(api_key)s"

    def test_list(self):
        zip_code = ZipCodeFactory.create()
        response = self.client.get(self.url)
        expected = '{"objects": [%s]}' % zip_code.jsonify()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected)

    def test_detail(self):
        zip_code = ZipCodeFactory.create()
        url = self.url_with_zip_code % {'zip_code': zip_code.zip_code,
                                        'api_key': self.api_key}
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, zip_code.jsonify())
