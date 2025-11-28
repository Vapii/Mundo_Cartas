from django import forms
from .models import ItemCarrito

class ItemCarritoForm(forms.ModelForm):
    class Meta:
        model = ItemCarrito
        fields = ['producto', 'cantidad']
