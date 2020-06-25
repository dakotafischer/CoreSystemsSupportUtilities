from django.contrib import admin
from saml_post.models import SamlProfile, SamlProfileAttribute

admin.site.register(SamlProfile)
admin.site.register(SamlProfileAttribute)
