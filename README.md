# iClinic ZipCode API

[![Build Status](https://travis-ci.org/mdsrosa/iclinic_cep_webservice.svg)](https://travis-ci.org/mdsrosa/iclinic_cep_webservice) [![Coverage Status](https://coveralls.io/repos/mdsrosa/iclinic_cep_webservice/badge.svg?branch=master&service=github)](https://coveralls.io/github/mdsrosa/iclinic_cep_webservice?branch=master) [![Django version](https://img.shields.io/badge/Django-1.9.1-blue.svg)](https://docs.djangoproject.com/en/1.9/) [![Restless version](https://img.shields.io/badge/Restless-2.0.1-green.svg)](http://restless.readthedocs.org/en/latest/index.html)

Simple web service that collects zip code informations from a public API and stores in a database.

# Installation
###### **Considering you already have a Python development environment setup.**

```bash
$ git clone https://github.com/mdsrosa/iclinic_cep_webservices.git iclinic_webservices
$ cd iclinic_webservices
$ mkvirtualenv iclinic_webservices
$ pip install -r requirements/development.txt
```

### Generate your API Key

```bash
$ python manage.py createapikey
API Key created: d41d8cd98f00b204e9800998ecf8427e
```

### Running Locally
```bash
$ python manage.py migrate
$ python manage.py runserver
```

# Endpoints

#### GET /zipcodes/

This endpoint lists all routes in the database.

#### cURL Example

```bash
$ curl -i http://localhost:8000/zipcodes/?api_key=d41d8cd98f00b204e9800998ecf8427e
```

#### Response Example
```bash
{
    "objects": [
        {
            "city": "Araraquara",
            "neighborhood": "Centro",
            "state": "SP",
            "address": "Rua Padre Duarte",
            "id": 1,
            "zip_code": "14800360"
        },
        {
            "city": "Ribeirão Preto",
            "neighborhood": "Jardim América",
            "state": "SP",
            "address": "Avenida Presidente Vargas",
            "id": 2,
            "zip_code": "14020260"
        }
    ]
}
```

#### GET `/zipcodes/<zip_code>`
This endpoint returns the details of a zipcode.

##### cURL Example
```bash
$ curl -i http://localhost:8000/zipcode/14020260/?api_key=d41d8cd98f00b204e9800998ecf8427e
```

##### Response Example
```bash
{
    "city": "Araraquara",
    "neighborhood": "Centro",
    "state": "SP",
    "address": "Rua Padre Duarte",
    "id": 1,
    "zip_code": "14800360"
}
```

#### POST `/zipcodes/`
This endpoint creates a new zipcode.

#### Fields

Name            | Type | Description | Example
----------------|------|------------ |--------
**zipcode**| _string_ | The zip code| `"14800360"`

##### cURL Example
```bash
$ curl -i -H "Content-Type: application/json" -X POST http://localhost:8000/zipcodes/?api_key=d41d8cd98f00b204e9800998ecf8427e -d '{"zip_code":"14800360"}'
```

##### Response Example
```bash
{
    "city": "Araraquara",
    "neighborhood": "Centro",
    "state": "SP",
    "address": "Rua Padre Duarte",
    "id": 1,
    "zip_code": "14800360"
}
```

#### DELETE `/zipcodes/<zip_code>`
This endpoint deletes a zipcode.

##### cURL Example
```bash
$ curl -X DELETE http://localhost:8000/zipcodes/14800360?api_key=d41d8cd98f00b204e9800998ecf8427e
```

# Tests
```bash
python manage.py --pattern=*_test.py
```
