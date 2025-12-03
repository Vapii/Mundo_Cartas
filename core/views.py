from django.shortcuts import render
from .models import Noticia, Banner
from django.shortcuts import render, get_object_or_404

from productos.models import Producto

def home(request):
    banners = Banner.objects.filter(activo=True)
    noticias = Noticia.objects.order_by('-fecha_publicacion')[:5]
    productos_recientes = Producto.objects.order_by('-creado')[:10]
    productos = Producto.objects.order_by('?')[:10]
    return render(request, 'core/home.html', {
        'banners': banners,
        'noticias': noticias,
        'productos': productos,
        'productos_recientes': productos_recientes,
    })


def noticias(request):
    ultima = Noticia.objects.order_by('-fecha_publicacion').first()
    return render(request, 'core/noticias.html', {'noticia': ultima})


def todas_las_noticias(request):
    noticias = Noticia.objects.order_by('-fecha_publicacion')
    return render(request, 'core/todas_noticias.html', {'noticias': noticias})


