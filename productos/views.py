from django.shortcuts import render, get_object_or_404
# IMPORTANTE: Asegúrate de importar Categoria de tu models.py
from .models import Producto, Categoria 

# =======================================================
# 1. FUNCIÓN PARA LA LISTA DE PRODUCTOS (CATÁLOGO)
# =======================================================
def lista_productos(request):
    # 1. Inicialmente, obtenemos todos los productos
    productos = Producto.objects.all()
    
    # 2. Lógica para el FILTRO DE ORDENACIÓN
    # Recoge el parámetro 'orden' de la URL (ej: ?orden=precio_desc), con 'nombre' como default
    orden = request.GET.get('orden', 'nombre') 
    
    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio') # '-' para descendente (mayor a menor)
    elif orden == 'novedad':
        productos = productos.order_by('-creado') # Asume que 'creado' está en models.py
    else:
        productos = productos.order_by('nombre')
        
    # 3. Lógica para el FILTRO POR CATEGORÍA
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        # Filtramos los productos que están asociados a esa categoría
        productos = productos.filter(categorias__id=categoria_id)

    # 4. Obtener todas las categorías para llenar el filtro (dropdown)
    categorias = Categoria.objects.all() 
    
    # 5. Preparamos el contexto
    context = {
        'productos': productos,
        'categorias': categorias,
        'orden_seleccionado': orden, 
        # Convierte el ID a entero para usarlo en el template
        'categoria_seleccionada_id': int(categoria_id) if categoria_id else None 
    }
    
    return render(request, 'productos/lista.html', context)

# =======================================================
# 2. FUNCIÓN PARA EL DETALLE DE UN PRODUCTO
# =======================================================
def detalle_producto(request, producto_id):
    # Esta función ya estaba correcta, solo la incluimos para mantener tu app funcionando
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/detail.html', {'producto': producto})