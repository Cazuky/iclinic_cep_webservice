from django.conf.urls import url, include
from iclinic_webservices.webservices.zipcodes.api import ZipCodeResource


urlpatterns = [
    url(r'zipcodes/', include(ZipCodeResource.urls()))
]
