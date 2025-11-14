from django.shortcuts import render
from .models import Noticia, Banner
from django.shortcuts import render, get_object_or_404

from productos.models import Producto

def home(request):
    banners = Banner.objects.filter(activo=True)
    noticias = Noticia.objects.order_by('-fecha_publicacion')[:5]
    productos = Producto.objects.order_by('?')[:10]
    return render(request, 'core/home.html', {
        'banners': banners,
        'noticias': noticias,
        'productos': productos,
    })


def noticias(request):
    todas = Noticia.objects.order_by('-fecha_publicacion')
    return render(request, 'core/noticias.html', {'noticias': todas})

def noticia_detail(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    return render(request, 'core/noticia_detail.html', {'noticia': noticia})

