"""
    zipcode_resource_test.py
    Test file for the ZipCodeResource class
"""
import json

from django.test import TestCase, Client

from .factories import ZipCodeFactory, ApiKeyFactory
from iclinic_webservices.webservices.zipcodes.models import ZipCode


class ZipCodeResourceTestCase(TestCase):
    """
        TestCase for the ZipCode API
    """
    def setUp(self):
        self.client = Client()
        self.api_key = ApiKeyFactory.create()
        self.url = "/zipcodes/?api_key=%s" % self.api_key
        self.url_with_limit = "/zipcodes/?limit=%(limit)s&api_key=%(api_key)s"
        self.url_with_zipcode = "/zipcodes/%(zip_code)s/?api_key=%(api_key)s"
        self.fake_zipcode = '000-12345'

    def test_list(self):
        """
            Tests for the /zipcodes/ endpoint
        """
        zip_code = ZipCodeFactory.create()
        response = self.client.get(self.url)
        expected = '{"objects": [%s]}' % zip_code.jsonify()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected)

    def test_list_with_limit(self):
        """
            Tests for the /zipcodes/?limit=XXX endpoint
        """
        zip_codes = [
            ZipCodeFactory.create(),
            ZipCodeFactory.create(),
            ZipCodeFactory.create()
        ]

        url = self.url_with_limit % {'limit': 1, 'api_key': self.api_key}
        response = self.client.get(url)
        expected = '{"objects": [%s]}' % zip_codes[2].jsonify()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected)

    def test_create(self):
        """
            Tests for the /zipcodes/ endpoint with POST method
        """
        zip_code_json = json.dumps({"zip_code": "14020260"})
        response = self.client.post(self.url,
                                    zip_code_json,
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)

        zip_code = ZipCode.objects.get(zip_code="14020260")
        expected = zip_code.jsonify()

        self.assertJSONEqual(response.content, expected)

    def teste_delete(self):
        """
            Tests for the /zipcodes/<zip_code> endpoint with DELETE method
        """
        zip_code = ZipCodeFactory.create()
        url = self.url_with_zipcode % {'zip_code': zip_code.zip_code,
                                       'api_key': self.api_key}

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

    def test_detail(self):
        """
            Tests for the /zipcodes/<zip_code> endpoint
        """
        zip_code = ZipCodeFactory.create()
        url = self.url_with_zipcode % {'zip_code': zip_code.zip_code,
                                       'api_key': self.api_key}
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, zip_code.jsonify())

    def test_create_zipcode_duplicated(self):
        """
            Tests for the /zipcodes/ endpoint with POST method trying to insert
            the same zipcode into the database.
        """
        zip_code_json = json.dumps({"zip_code": "14800360"})

        # create zipcode successfullly
        response = self.client.post(self.url, zip_code_json,
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)

        # fails to create because already exists
        response = self.client.post(self.url, zip_code_json,
                                    content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_detail_not_found(self):
        """
            Tests for the /zipcodes/<zip_code> when zip_code does not exist
        """
        zip_code = '00000000'
        url = self.url_with_zipcode % {'zip_code': zip_code,
                                       'api_key': self.api_key}
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_delete_not_found(self):
        """
            Tests for the /zipcodes/<zip_code> with DELETE method
            when zip_code does not exist
        """
        zip_code = '00000000'
        url = self.url_with_zipcode % {'zip_code': zip_code,
                                       'api_key': self.api_key}
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

    def test_create_invalid_format(self):
        """
            Tests for the /zipcodes/ with the POST method when zip_code
            doesn't have a valid format
        """
        zip_code_json = json.dumps({'zip_code': self.fake_zipcode})
        error_message = "Invalid %s zip code format." % self.fake_zipcode

        response = self.client.post(self.url, zip_code_json,
                                    content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn(error_message, response.content)

    def test_create_not_found_postmon(self):
        """
            Tests for the /zipcodes/ with the POST method when Postmon
            doesn't find the zip_code
        """
        zip_code = '00000-123'
        zip_code_json = json.dumps({'zip_code': zip_code})
        error_message = "Zipcode %s not found in Postmon." % zip_code

        response = self.client.post(self.url, zip_code_json,
                                    content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn(error_message, response.content)
