from django.shortcuts import render, redirect, get_object_or_404
from .models import RegistroAdmin
from productos.models import Producto, Categoria
from usuario.models import Usuario
from django.contrib.auth.models import Group
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_admin(request):
    registros = RegistroAdmin.objects.order_by('-fecha')[:20]
    return render(request, 'admin_panel/dashboard.html', {'registros': registros})

@staff_member_required
def admin_productos(request):
    productos = Producto.objects.all().order_by('-creado')
    return render(request, 'admin_panel/admin_productos.html', {'productos': productos})

@staff_member_required
def admin_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'admin_panel/admin_categorias.html', {'categorias': categorias})

@staff_member_required
def admin_compras(request):
    return render(request, 'admin_panel/admin_compras.html')



# P R O D U C T O S  


@staff_member_required
def crear_producto(request):
    categorias = Categoria.objects.all()

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")
        imagen = request.FILES.get("imagen")
        categorias_seleccionadas = request.POST.getlist("categorias")

        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen=imagen
        )
        producto.categorias.set(categorias_seleccionadas)


    return render(request, 'admin_panel/crear_producto.html', {"categorias": categorias})



@staff_member_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all()

    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio")
        producto.stock = request.POST.get("stock")

        imagen = request.FILES.get("imagen")
        if imagen:
            producto.imagen = imagen
        producto.save()

        categorias_seleccionadas = request.POST.getlist("categorias")
        producto.categorias.set(categorias_seleccionadas)

        return redirect('admin_productos')

    return render(request, 'admin_panel/editar_producto.html', {
        "producto": producto,
        "categorias": categorias,
    })

@staff_member_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('admin_productos')

# C A T E G O R I A S  

@staff_member_required
def crear_categoria(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")

        Categoria.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )

    return render(request, 'admin_panel/crear_categoria.html')


@staff_member_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":
        categoria.nombre = request.POST.get("nombre")
        categoria.descripcion = request.POST.get("descripcion")
        categoria.save()
        return redirect('admin_categorias')

    return render(request, 'admin_panel/editar_categoria.html', {
        "categoria": categoria
    })


@staff_member_required
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('admin_categorias')

# U S U A R I O S


@staff_member_required
def admin_usuarios(request):
    usuario = Usuario.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/admin_usuarios.html', {'usuario': usuario})


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

    return render(request, 'admin_panel/editar_grupo_usuario.html', {
        'usuario': usuario,
        'grupos': grupos
    })

@staff_member_required
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('admin_usuarios')
