from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen', 'categorias']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'categorias': forms.CheckboxSelectMultiple()
        }
