from __future__ import unicode_literals

from django.db import models


class ApiKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_keys'

    def __unicode__(self):
        return self.key
