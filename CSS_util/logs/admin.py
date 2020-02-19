from django.contrib import admin
from .models import LoggedApp, AuditLog, ProcessedLog

admin.site.register(LoggedApp)
admin.site.register(AuditLog)
admin.site.register(ProcessedLog)