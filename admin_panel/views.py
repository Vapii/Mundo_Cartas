from django.shortcuts import render, redirect, get_object_or_404
from .models import RegistroAdmin
from usuario.models import Usuario
from django.contrib.auth.models import Group
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from core.models import Noticia, Banner
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pagos.models import Pago, ItemCompra, Compra
import json
from django.db.models import Q
from utils.decorators import solo_admins
from productos.models import Producto, Categoria, Proveedor
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.utils import timezone


@solo_admins
@staff_member_required
def admin_compras(request):
    query = request.GET.get("q")
    compras = Pago.objects.select_related("usuario").order_by("-fecha")
    if query:
        compras = compras.filter(
            Q(id__icontains=query) |
            Q(buy_order__icontains=query) |
            Q(usuario__username__icontains=query) |
            Q(usuario__email__icontains=query)
        )

    return render(request, "admin_panel/compras/admin_compras.html", {
        "compras": compras,
        "query": query
    })

@solo_admins
@staff_member_required
def dashboard_admin(request):
    registros = RegistroAdmin.objects.order_by('-fecha')[:20]
    return render(request, 'admin_panel/dashboard.html', {'registros': registros})

@solo_admins
@staff_member_required
def admin_productos(request):
    query = request.GET.get("q")
    productos = Producto.objects.all().order_by('-creado')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(categorias__nombre__icontains=query) |
            Q(proveedor__nombre__icontains=query)
        ).distinct()

    return render(request, 'admin_panel/productos/admin_productos.html', {
        'productos': productos,
        'query': query
    })

@solo_admins
@staff_member_required
def admin_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'admin_panel/categorias/admin_categorias.html', {'categorias': categorias})

@solo_admins
@staff_member_required
def admin_usuarios(request):
    query = request.GET.get("q")
    usuario = Usuario.objects.all().order_by('-date_joined')
    if query:
        usuario = usuario.filter(username__icontains=query)

    return render(request, 'admin_panel/usuarios/admin_usuarios.html', {
        'usuario': usuario,
        'query': query
    })

@solo_admins
@staff_member_required
def listar_noticias(request):
    noticias = Noticia.objects.order_by('-fecha_publicacion')
    return render(request, 'admin_panel/noticias/admin_noticias.html', {'noticias': noticias})

@solo_admins
@staff_member_required
def listar_banners(request):
    banners = Banner.objects.order_by('-id')
    return render(request, 'admin_panel/banner/admin_banner.html', {'banners': banners})

@solo_admins
@staff_member_required
def proveedores_list(request):
    query = request.GET.get('q')
    if query:
        proveedores = Proveedor.objects.filter(
            Q(nombre__icontains=query)
        )
    else:
        proveedores = Proveedor.objects.all()
    return render(request, 'admin_panel/proveedor/admin_proveedores.html', {'proveedores': proveedores})


# P R O D U C T O S  

@solo_admins
@staff_member_required
def crear_producto(request):
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        stock_manual = int(request.POST.get("stock") or 0)
        imagen = request.FILES.get("imagen")
        categorias_seleccionadas = request.POST.getlist("categorias")
        proveedor_id = request.POST.get("proveedor")

        if not nombre or not categorias_seleccionadas or not proveedor_id:
            messages.error(request, "Nombre, proveedor y al menos una categoría son obligatorios")
            return render(request, 'admin_panel/productos/crear_producto.html', {
                "categorias": categorias,
                "proveedores": proveedores
            })

        if Producto.objects.filter(nombre__iexact=nombre).exists():
            messages.error(request, "Ya existe un producto con ese nombre")
            return render(request, 'admin_panel/productos/crear_producto.html', {
                "categorias": categorias,
                "proveedores": proveedores
            })

        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock_manual,
            imagen=imagen,
            proveedor_id=proveedor_id
        )
        producto.categorias.set(categorias_seleccionadas)

        messages.success(request, "Producto creado correctamente.")
        return redirect("admin_productos")

    return render(request, 'admin_panel/productos/crear_producto.html', {
        "categorias": categorias,
        "proveedores": proveedores
    })

@solo_admins
@staff_member_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == "POST":
        nuevo_nombre = request.POST.get("nombre")
        nueva_descripcion = request.POST.get("descripcion")
        nuevo_precio = request.POST.get("precio")
        nuevo_stock = request.POST.get("stock")
        proveedor_id = request.POST.get("proveedor")
        imagen = request.FILES.get("imagen")
        categorias_seleccionadas = request.POST.getlist("categorias")

        if not nuevo_nombre or not proveedor_id or not categorias_seleccionadas:
            messages.error(request, "Nombre, proveedor y al menos una categoría son obligatorios")
            return render(request, 'admin_panel/productos/editar_producto.html', {
                "producto": producto,
                "categorias": categorias,
                "proveedores": proveedores
            })

        if Producto.objects.filter(nombre__iexact=nuevo_nombre).exclude(id=id).exists():
            messages.error(request, "Ya existe otro producto con ese nombre")
            return render(request, 'admin_panel/productos/editar_producto.html', {
                "producto": producto,
                "categorias": categorias,
                "proveedores": proveedores
            })

        producto.nombre = nuevo_nombre
        producto.descripcion = nueva_descripcion
        producto.precio = nuevo_precio
        producto.stock = nuevo_stock
        producto.proveedor_id = proveedor_id
        if imagen:
            producto.imagen = imagen
        producto.save()
        producto.categorias.set(categorias_seleccionadas)
        messages.success(request, "Producto actualizado correctamente")
        return redirect('admin_productos')

    return render(request, 'admin_panel/productos/editar_producto.html', {
        "producto": producto,
        "categorias": categorias,
        "proveedores": proveedores
    })



@solo_admins
@staff_member_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('admin_productos')


# C O M P R A S

@solo_admins
@staff_member_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Pago, id=compra_id)
    productos = ItemCompra.objects.filter(pago=compra)

    for item in productos:
        item.subtotal = item.producto.precio * item.cantidad

    return render(request, "admin_panel/compras/detail_compra.html", {
        "compra": compra,
        "productos": productos
    })


# C A T E G O R I A S  

@solo_admins
@staff_member_required
def crear_categoria(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        if not nombre:
            messages.error(request, "El nombre es obligatorio")
            return render(request, 'admin_panel/categorias/crear_categoria.html')

        if Categoria.objects.filter(nombre__iexact=nombre).exists():
            messages.error(request, "Ya existe una categoría con ese nombre")
            return render(request, 'admin_panel/categorias/crear_categoria.html')

        Categoria.objects.create(nombre=nombre, descripcion=descripcion)
        messages.success(request, "Categoría creada correctamente")
        return redirect('admin_categorias')

    return render(request, 'admin_panel/categorias/crear_categoria.html')


@solo_admins
@staff_member_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == "POST":
        nuevo_nombre = request.POST.get("nombre")
        nueva_descripcion = request.POST.get("descripcion")

        if not nuevo_nombre:
            messages.error(request, "El nombre es obligatorio")
            return render(request, 'admin_panel/categorias/editar_categoria.html', {"categoria": categoria})

        if Categoria.objects.filter(nombre__iexact=nuevo_nombre).exclude(id=id).exists():
            messages.error(request, "Ya existe otra categoría con ese nombre")
            return render(request, 'admin_panel/categorias/editar_categoria.html', {"categoria": categoria})

        categoria.nombre = nuevo_nombre
        categoria.descripcion = nueva_descripcion
        categoria.save()
        messages.success(request, "Categoría actualizada correctamente")
        return redirect('admin_categorias')

    return render(request, 'admin_panel/categorias/editar_categoria.html', {"categoria": categoria})


@solo_admins
@staff_member_required
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('admin_categorias')


# U S U A R I O S

@solo_admins
@staff_member_required
def crear_usuario_admin(request):
    grupos = Group.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        grupo_id = request.POST.get('grupo')

        if not username or not email or not password or not grupo_id:
            messages.error(request, "Todos los campos son obligatorios")
            return redirect('crear_usuario')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, f"El usuario '{username}' ya existe")
            return redirect('crear_usuario')

        try:
            grupo = Group.objects.get(id=grupo_id)
        except Group.DoesNotExist:
            messages.error(request, "Grupo seleccionado no válido")
            return redirect('crear_usuario')
        nuevo_usuario = Usuario.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        nuevo_usuario.groups.add(grupo)
        RegistroAdmin.objects.create(
            usuario=request.user,
            accion=f"Creó usuario '{username}' y lo asignó al grupo '{grupo.name}'"
        )
        messages.success(request, f"Usuario '{username}' creado correctamente")
        return redirect('admin_usuarios')

    return render(request, 'admin_panel/usuarios/crear_user.html', {
        'grupos': grupos
    })


@solo_admins
@staff_member_required
def editar_grupo_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    grupos = Group.objects.all()
    if request.method == 'POST':
        grupo_id = request.POST.get('grupo')
        if grupo_id:
            nuevo_grupo = get_object_or_404(Group, id=grupo_id)
            usuario.groups.clear()
            usuario.groups.add(nuevo_grupo)
        return redirect('admin_usuarios')

    return render(request, 'admin_panel/usuarios/editar_grupo_usuario.html', {
        'usuario': usuario,
        'grupos': grupos
    })


@solo_admins
@staff_member_required
def toggle_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.is_active = not usuario.is_active  
    usuario.save()
    return redirect('admin_usuarios')

@solo_admins
@staff_member_required
def historial_compras_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    compras = Pago.objects.filter(usuario=usuario).order_by("-fecha")

    return render(request, "admin_panel/usuarios/historial_user.html", {
        "usuario": usuario,
        "compras": compras
    })


# N O T I C I A S

@solo_admins
@staff_member_required
def crear_noticia(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')

        if not titulo or not descripcion:
            messages.error(request, "Título y descripción son obligatorios")
            return render(request, 'admin_panel/noticias/crear_noticias.html')

        if Noticia.objects.filter(titulo__iexact=titulo).exists():
            messages.error(request, "Ya existe una noticia con ese título")
            return render(request, 'admin_panel/noticias/crear_noticias.html')

        Noticia.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            imagen=imagen
        )
        messages.success(request, "Noticia creada correctamente")
        return redirect('admin_noticias')

    return render(request, 'admin_panel/noticias/crear_noticias.html')


@solo_admins
@staff_member_required
def editar_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    if request.method == 'POST':
        nuevo_titulo = request.POST.get('titulo')
        nueva_descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')

        if not nuevo_titulo or not nueva_descripcion:
            messages.error(request, "Título y descripción son obligatorios")
            return render(request, 'admin_panel/noticias/editar_noticias.html', {'noticia': noticia})

        if Noticia.objects.filter(titulo__iexact=nuevo_titulo).exclude(id=id).exists():
            messages.error(request, "Ya existe otra noticia con ese título")
            return render(request, 'admin_panel/noticias/editar_noticias.html', {'noticia': noticia})

        noticia.titulo = nuevo_titulo
        noticia.descripcion = nueva_descripcion
        if imagen:
            noticia.imagen = imagen
        noticia.save()

        messages.success(request, "Noticia actualizada")
        return redirect('admin_noticias')

    return render(request, 'admin_panel/noticias/editar_noticias.html', {'noticia': noticia})


@solo_admins
@staff_member_required
def eliminar_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    noticia.delete()
    messages.info(request, "Noticia eliminada")
    return redirect('admin_noticias')


# B A N N E R S

@solo_admins
@staff_member_required
def crear_banner(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        imagen = request.FILES.get('imagen')
        activo = bool(request.POST.get('activo'))

        if not titulo:
            messages.error(request, "El título es obligatorio")
            return render(request, 'admin_panel/banner/crear_banner.html')

        if Banner.objects.filter(titulo__iexact=titulo).exists():
            messages.error(request, "Ya existe un banner con ese título")
            return render(request, 'admin_panel/banner/crear_banner.html')

        if not imagen:
            messages.error(request, "La imagen es obligatoria")
            return render(request, 'admin_panel/banner/crear_banner.html')

        Banner.objects.create(
            titulo=titulo,
            imagen=imagen,
            activo=activo
        )
        messages.success(request, "Banner creado correctamente")
        return redirect('admin_banners')

    return render(request, 'admin_panel/banner/crear_banner.html')


@solo_admins
@staff_member_required
def editar_banner(request, id):
    banner = get_object_or_404(Banner, id=id)

    if request.method == 'POST':
        banner.titulo = request.POST.get('titulo')
        banner.activo = bool(request.POST.get('activo'))

        imagen = request.FILES.get('imagen')
        if imagen:
            banner.imagen = imagen

        banner.save()
        messages.success(request, "Banner actualizado correctamente")
        return redirect('admin_banners')

    return render(request, 'admin_panel/banner/editar_banner.html', {
        "banner": banner
    })

@solo_admins
@staff_member_required
def eliminar_banner(request, id):
    banner = get_object_or_404(Banner, id=id)
    banner.delete()
    messages.info(request, "Banner eliminado")
    return redirect('admin_banners')

@solo_admins
@csrf_exempt  
@staff_member_required
def toggle_activo_banner(request, id):
    if request.method == 'POST':
        banner = get_object_or_404(Banner, id=id)
        data = json.loads(request.body)
        banner.activo = data.get('activo', False)
        banner.save()
        return JsonResponse({'status': 'ok'})
    
# P R O V E E D O R E S

@solo_admins
@staff_member_required
def crear_proveedor(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        contacto = request.POST.get("contacto")
        activo = bool(request.POST.get("activo"))

        if not nombre:
            messages.error(request, "El nombre es obligatorio")
            return render(request, "admin_panel/proveedor/crear_proveedor.html")

        if Proveedor.objects.filter(nombre__iexact=nombre).exists():
            messages.error(request, "Ya existe un proveedor con ese nombre")
            return render(request, "admin_panel/proveedor/crear_proveedor.html")

        Proveedor.objects.create(
            nombre=nombre,
            contacto=contacto,
            activo=activo
        )
        messages.success(request, "Proveedor creado correctamente")
        return redirect("admin_proveedores")

    return render(request, "admin_panel/proveedor/crear_proveedor.html")


@solo_admins
@staff_member_required
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)

    if request.method == "POST":
        nuevo_nombre = request.POST.get("nombre")
        nuevo_contacto = request.POST.get("contacto")
        activo = bool(request.POST.get("activo"))

        if not nuevo_nombre:
            messages.error(request, "El nombre es obligatorio")
            return render(request, "admin_panel/proveedor/editar_proveedor.html", {"proveedor": proveedor})

        if Proveedor.objects.filter(nombre__iexact=nuevo_nombre).exclude(id=id).exists():
            messages.error(request, "Ya existe otro proveedor con ese nombre")
            return render(request, "admin_panel/proveedor/editar_proveedor.html", {"proveedor": proveedor})

        proveedor.nombre = nuevo_nombre
        proveedor.contacto = nuevo_contacto
        proveedor.activo = activo
        proveedor.save()

        messages.success(request, "Proveedor actualizado correctamente")
        return redirect("admin_proveedores")

    return render(request, "admin_panel/proveedor/editar_proveedor.html", {"proveedor": proveedor})


@solo_admins
@staff_member_required
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()
    messages.success(request, "Proveedor eliminado correctamente.")
    return redirect("admin_proveedores")


# f i s i c a

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

# @solo_admins  # si tú lo tienes definido, déjalo
@staff_member_required
def admin_ventas_fisicas(request):
    query = request.GET.get("q")
    productos = Producto.objects.all()

    if query:
        productos = productos.filter(Q(nombre__icontains=query))

    if "carrito" not in request.session:
        request.session["carrito"] = []

    carrito = request.session["carrito"]

    # -----------------------------
    # AGREGAR AL CARRITO
    # -----------------------------
    if request.method == "POST" and "agregar" in request.POST:
        producto_id = int(request.POST.get("producto_id"))
        cantidad = int(request.POST.get("cantidad"))

        producto = get_object_or_404(Producto, id=producto_id)
        stock = int(producto.stock)

        if stock <= 0:
            messages.error(request, f"'{producto.nombre}' no tiene stock disponible.")
            return redirect("admin_ventas_fisicas")

        # cantidad actual en carrito
        actual = 0
        for item in carrito:
            if item["producto_id"] == producto_id:
                actual = int(item["cantidad"])
                break

        nueva = actual + cantidad

        # limitar al stock
        if nueva > stock:
            nueva = stock
            messages.warning(request, f"Solo hay {stock} unidades disponibles de {producto.nombre}.")

        encontrado = False
        for item in carrito:
            if item["producto_id"] == producto_id:
                item["cantidad"] = nueva
                encontrado = True
                break

        if not encontrado:
            carrito.append({"producto_id": producto_id, "cantidad": nueva})

        request.session["carrito"] = carrito
        request.session.modified = True
        return redirect("admin_ventas_fisicas")

    # -----------------------------
    # ELIMINAR ITEM COMPLETO (NUEVO)
    # -----------------------------
    if request.method == "POST" and "eliminar_item" in request.POST:
        producto_id = int(request.POST.get("producto_id"))

        nuevo_carrito = []
        for item in carrito:
            if item["producto_id"] != producto_id:
                nuevo_carrito.append(item)

        request.session["carrito"] = nuevo_carrito
        request.session.modified = True
        return redirect("admin_ventas_fisicas")

    # -----------------------------
    # REGISTRAR COMPRA
    # -----------------------------
    if request.method == "POST" and "registrar_compra" in request.POST:
        # 1) Revalidar stock real antes de comprar
        for item in carrito:
            p = get_object_or_404(Producto, id=item["producto_id"])
            if int(item["cantidad"]) > int(p.stock):
                messages.error(
                    request,
                    f"Stock insuficiente para '{p.nombre}'. Disponible: {p.stock}, en carrito: {item['cantidad']}."
                )
                return redirect("admin_ventas_fisicas")

        # 2) Registrar compra + pago + descontar stock
        for item in carrito:
            producto = get_object_or_404(Producto, id=item["producto_id"])
            cantidad_item = int(item["cantidad"])

            compra = Compra.objects.create(
                producto=producto,
                cantidad=cantidad_item,
                vendedor=request.user
            )

            pago = Pago.objects.create(
                usuario=request.user,
                monto=producto.precio * cantidad_item,
                metodo="EFECTIVO",
                estado="COMPLETADO",
                codigo_autorizacion=f"COMPRA-{compra.id}",
                buy_order=f"COMPRA-{compra.id}"
            )

            compra.pago = pago
            compra.save()

            # DESCONTAR STOCK
            producto.stock = int(producto.stock) - cantidad_item
            producto.save()

        request.session["carrito"] = []
        request.session.modified = True
        messages.success(request, "Compra registrada y stock actualizado.")
        return redirect("admin_ventas_fisicas")

    # -----------------------------
    # QUITAR 1 UNIDAD
    # -----------------------------
    if request.method == "POST" and "quitar" in request.POST:
        producto_id = int(request.POST.get("producto_id"))
        nuevo_carrito = []
        for item in carrito:
            if item["producto_id"] == producto_id:
                if item["cantidad"] > 1:
                    item["cantidad"] -= 1
                    nuevo_carrito.append(item)
                # si queda en 0, no se agrega => desaparece
            else:
                nuevo_carrito.append(item)

        request.session["carrito"] = nuevo_carrito
        request.session.modified = True
        return redirect("admin_ventas_fisicas")

    # -----------------------------
    # SUMAR 1 UNIDAD
    # -----------------------------
    if request.method == "POST" and "sumar" in request.POST:
        producto_id = int(request.POST.get("producto_id"))

        producto = get_object_or_404(Producto, id=producto_id)
        stock = int(producto.stock)

        for item in carrito:
            if item["producto_id"] == producto_id:
                if int(item["cantidad"]) >= stock:
                    messages.warning(request, f"No puedes sumar más: stock máximo {stock} para {producto.nombre}.")
                else:
                    item["cantidad"] = int(item["cantidad"]) + 1
                break

        request.session["carrito"] = carrito
        request.session.modified = True
        return redirect("admin_ventas_fisicas")

    # -----------------------------
    # ARMAR CARRITO PARA TEMPLATE
    # -----------------------------
    carrito_enriquecido = []
    total = 0
    for item in carrito:
        try:
            producto = productos.get(id=item["producto_id"])
            subtotal = producto.precio * item["cantidad"]
            total += subtotal
            carrito_enriquecido.append({
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "imagen": producto.imagen.url if producto.imagen else None,
                "cantidad": item["cantidad"],
                "subtotal": subtotal
            })
        except Producto.DoesNotExist:
            continue

    return render(request, "admin_panel/fisica/crear_fisica.html", {
        "productos": productos,
        "query": query,
        "carrito": carrito_enriquecido,
        "total": total
    })
