from django.db import models



class LoggedApp(models.Model):
    environment = models.CharField(max_length=200)
    log_type = models.CharField(max_length=200)
    log_location = models.CharField(max_length=200)
    log_file_mask = models.CharField(max_length=200)
    last_updated = models.DateTimeField('last updated date')

    def __str__(self):
        return str(self.application) + ' -- ' + str(self.environment) + ' -- ' + str(self.log_type)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['application', 'environment', 'log_type'], name='Unique LoggedApp Constraint')
        ]

class AuditLog(models.Model):
    logged_app = models.ForeignKey(LoggedApp, on_delete=models.CASCADE)
    environment = models.CharField(max_length=200)
    logged_date = models.DateTimeField('logged date')
    entity_id = models.CharField(max_length=200)
    saml_subject = models.CharField(max_length=200)
    relay_state = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    role = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    adapter = models.CharField(max_length=200, blank=True)
    logged_data = models.TextField(blank=True)
    pf_id = models.CharField(max_length=200)

    def __str__(self):
        return str(self.logged_app) + ' -- ' + self.environment + ' -- ' + str(self.logged_date) + ' -- ' + self.entity_id + ' -- ' + self.saml_subject

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['logged_app', 'logged_date', 'entity_id', 'saml_subject'], name='Unique AuditLog Constraint')
        ]

class ProcessedLog(models.Model):
    logged_app = models.ForeignKey(LoggedApp, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    log_type = models.CharField(max_length=50)
    logged_date = models.DateField('logged date')
    processed_date = models.DateTimeField('processed date')

    def __str__(self):
        return str(self.file_name)
