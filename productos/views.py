from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria
from django.db.models import Q


def lista_productos(request):

    productos = Producto.objects.all()
    orden = request.GET.get('orden', 'nombre') 
    
    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'novedad':
        productos = productos.order_by('-creado')
    else:
        productos = productos.order_by('nombre')
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categorias__id=categoria_id)
    categorias = Categoria.objects.all() 
    context = {
        'productos': productos,
        'categorias': categorias,
        'orden_seleccionado': orden, 
        'categoria_seleccionada_id': int(categoria_id) if categoria_id else None 
    }
    
    return render(request, 'productos/lista.html', context)


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/detail.html', {'producto': producto})

def buscar_productos(request):
    query = request.GET.get('q', '')
    resultados = Producto.objects.filter(
        Q(nombre__icontains=query) |
        Q(categorias__nombre__icontains=query)
    ).distinct()

    return render(request, 'productos/busqueda.html', {
        'resultados': resultados,
        'query': query
    })