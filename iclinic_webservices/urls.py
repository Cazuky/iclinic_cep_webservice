from django.conf.urls import url
from iclinic_webservices.webservices.zipcodes.api import ZipCodeResource


urlpatterns = [
    url(r'zipcodes/$', ZipCodeResource.as_list()),
    url(r'zipcodes/(?P<zip_code>\d{8})/$', ZipCodeResource.as_detail())
]
