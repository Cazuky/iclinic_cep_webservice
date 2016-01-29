from __future__ import unicode_literals

from django.db import models


class ZipCode(models.Model):

    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=9, unique=True)
    neighborhood = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'zip_codes'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.zip_code
