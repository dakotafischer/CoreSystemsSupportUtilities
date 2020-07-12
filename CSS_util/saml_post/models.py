import datetime

from django.db import models
from django.utils import timezone

class SamlProfile(models.Model):
    name = models.CharField(max_length=200, unique=True)
    issuer_id = models.CharField(max_length=200)
    saml_subject = models.CharField(max_length=200)
    audience_id = models.CharField(max_length=200)
    acs_endpoint = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField('last updated', auto_now_add=True)

    def add_saml_profile_attributes(self, attributes):
        for attribute in attributes:
            # add attribute
            pass
    
    def __str__(self):
        return self.name

class SamlProfileAttribute(models.Model):
    saml_profile_id = models.ForeignKey(SamlProfile, on_delete=models.CASCADE)
    attribute_name = models.CharField(max_length=200)
    attribute_value = models.CharField(max_length=200)
