from django import forms

class AuditLogForm(forms.Form):
    entity_id = forms.CharField(label='Entity ID', max_length=100, required=False)
