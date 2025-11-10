from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'monto', 'metodo', 'fecha')
    search_fields = ('usuario__username', 'codigo_autorizacion')
    list_filter = ('metodo', 'fecha')
