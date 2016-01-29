import hashlib
import random
import string

from django.core.management.base import BaseCommand

from iclinic_webservices.webservices.apikeys.models import ApiKey



class Command(BaseCommand):
    help = "Creates a API Key"

    def random_string(self, length=10):
        return ''.join(random.choice(string.ascii_letters) for x in xrange(length))

    def handle(self, *args, **options):
        md5 = hashlib.md5()
        md5.update(self.random_string())

        api_key = ApiKey.objects.create(key=md5.hexdigest(), active=True)

        self.stdout.write(self.style.SUCCESS("API Key created: %s" % api_key.key))
