from django.contrib import admin
from django.utils.html import format_html
from .models import Noticia, Banner

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_publicacion')
    search_fields = ('titulo',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'preview')
    list_editable = ('activo',)
    list_filter = ('activo',)
    ordering = ('titulo',)
    search_fields = ('titulo',)

    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="height: 50px;">', obj.imagen.url)
        return "Sin imagen"

    preview.short_description = "Vista previa"
