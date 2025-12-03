from django.contrib import admin
from .models import ItemCarrito

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad')
    search_fields = ('usuario__username', 'producto__nombre')
