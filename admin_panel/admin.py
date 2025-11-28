from django.contrib import admin
from .models import RegistroAdmin

@admin.register(RegistroAdmin)
class RegistroAdminAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha')
    search_fields = ('usuario__username', 'accion')
    list_filter = ('fecha',)
