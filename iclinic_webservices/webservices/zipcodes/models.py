from __future__ import unicode_literals
import json

from django.db import models

from collections import OrderedDict


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

    def jsonify(self):
        # fields are this ordered because restless can't
        # keep fields in the order the were defined
        zip_code = OrderedDict([
            ('city', self.city),
            ('neighborhood', self.neighborhood),
            ('state', self.state),
            ('address', self.address),
            ('id', self.pk),
            ('zip_code', self.zip_code)
        ])

        return json.dumps(zip_code)

    def save(self, *args, **kwargs):
        self.clean_zip_code()
        super(ZipCode, self).save(*args, **kwargs)

    def clean_zip_code(self):
        self.zip_code = self.zip_code.replace('-', '')
