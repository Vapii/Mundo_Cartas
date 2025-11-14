from django import forms
from .models import Noticia, Banner

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'contenido', 'imagen']

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['titulo', 'imagen', 'activo']
