from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, IntegerField, ExpressionWrapper, Sum
from .models import ItemCarrito
from productos.models import Producto
from django.contrib import messages

@login_required
def ver_carrito(request):
    items = ItemCarrito.objects.filter(usuario=request.user).annotate(
        subtotal=ExpressionWrapper(
            F('producto__precio') * F('cantidad'),
            output_field=IntegerField()
        )
    )
    total = items.aggregate(total=Sum('subtotal'))['total'] or 0
    total = int(total)

    return render(request, 'carrito/ver.html', {
        'items': items,
        'total': total
    })

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    item, creado = ItemCarrito.objects.get_or_create(
        usuario=request.user,
        producto=producto,
        defaults={'cantidad': 1}
    )

    if not creado:
        cantidad_actual = item.cantidad
        nueva_cantidad = cantidad_actual + 1

        if nueva_cantidad > producto.stock:
            messages.error(request, f"No puedes agregar más de {producto.stock} unidades de '{producto.nombre}'. Ya tienes {cantidad_actual} en el carrito.")
            return redirect('ver_carrito')

        item.cantidad = nueva_cantidad
        item.save(update_fields=['cantidad'])
    else:
        if producto.stock < 1:
            item.delete()
            messages.error(request, f"El producto '{producto.nombre}' no tiene stock disponible.")
            return redirect('ver_carrito')
    messages.success(request, f"'{producto.nombre}' agregado al carrito.")
    return redirect('ver_carrito')


@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save(update_fields=['cantidad'])
    else:
        item.delete()
    return redirect('ver_carrito')
