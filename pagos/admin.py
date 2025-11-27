from django.contrib import admin
from .models import Pago, ItemCompra

class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    extra = 0
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "monto", "estado", "buy_order", "fecha")
    search_fields = ('usuario__username', 'codigo_autorizacion')
    list_filter = ('metodo', 'fecha')
