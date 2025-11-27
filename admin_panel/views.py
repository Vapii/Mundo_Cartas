from django.shortcuts import render, redirect, get_object_or_404
from .models import RegistroAdmin
from productos.models import Producto, Categoria
from usuario.models import Usuario
from django.contrib.auth.models import Group
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import RegistroAdmin
from core.models import Noticia, Banner
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pagos.models import Pago, ItemCompra
import json
from django.db.models import Q
from utils.decorators import solo_admins




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
            Q(categorias__nombre__icontains=query)
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


# P R O D U C T O S  

@solo_admins
@staff_member_required
def crear_producto(request):
    categorias = Categoria.objects.all()

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")
        imagen = request.FILES.get("imagen")
        codigo_barras = request.POST.get("codigo_barras")
        categorias_seleccionadas = request.POST.getlist("categorias")

        # Validación opcional: evitar duplicados
        if Producto.objects.filter(codigo_barras=codigo_barras).exists():
            messages.error(request, "Ya existe un producto con ese código de barras.")
            return redirect("crear_producto")

        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen=imagen,
            codigo_barras=codigo_barras
        )
        producto.categorias.set(categorias_seleccionadas)

        messages.success(request, "Producto creado correctamente.")
        return redirect("admin_productos")

    return render(request, 'admin_panel/productos/crear_producto.html', {
        "categorias": categorias
    })



@solo_admins
@staff_member_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all()

    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio")
        producto.stock = request.POST.get("stock")

        codigo = request.POST.get("codigo_barras")
        producto.codigo_barras = codigo if codigo else None

        imagen = request.FILES.get("imagen")
        if imagen:
            producto.imagen = imagen

        producto.save()

        categorias_seleccionadas = request.POST.getlist("categorias")
        producto.categorias.set(categorias_seleccionadas)

        return redirect('admin_productos')

    return render(request, 'admin_panel/productos/editar_producto.html', {
        "producto": producto,
        "categorias": categorias,
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

        Categoria.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )

    return render(request, 'admin_panel/categorias/crear_categoria.html')


@solo_admins
@staff_member_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":
        categoria.nombre = request.POST.get("nombre")
        categoria.descripcion = request.POST.get("descripcion")
        categoria.save()
        return redirect('admin_categorias')

    return render(request, 'admin_panel/categorias/editar_categoria.html', {
        "categoria": categoria
    })


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

        # Validación de campos obligatorios
        if not username or not email or not password or not grupo_id:
            messages.error(request, "Todos los campos son obligatorios")
            return redirect('crear_usuario')

        # Validación de unicidad
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, f"El usuario '{username}' ya existe")
            return redirect('crear_usuario')

        try:
            grupo = Group.objects.get(id=grupo_id)
        except Group.DoesNotExist:
            messages.error(request, "Grupo seleccionado no válido")
            return redirect('crear_usuario')

        # Creación del usuario
        nuevo_usuario = Usuario.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        nuevo_usuario.groups.add(grupo)

        # Registro de acción administrativa
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
            return redirect('crear_noticia')

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
        noticia.titulo = request.POST.get('titulo')
        noticia.descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
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

        if not imagen:
            messages.error(request, "La imagen es obligatoria")
            return redirect('crear_banner')

        Banner.objects.create(
            titulo=titulo,
            imagen=imagen,
            activo=activo
        )
        messages.success(request, "Banner creado correctamente")
        return redirect('admin_banners')

    return render(request, 'admin_panel/banners/crear_banner.html')

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