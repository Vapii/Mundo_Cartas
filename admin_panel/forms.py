from django import forms
from .models import RegistroAdmin

class RegistroAdminForm(forms.ModelForm):
    class Meta:
        model = RegistroAdmin
        fields = ['accion']


