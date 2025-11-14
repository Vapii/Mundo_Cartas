from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_admin, name='dashboard'),

    # Productos
    path('productos/', views.admin_productos, name='admin_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:id>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),

    # Categorías
    path('categorias/', views.admin_categorias, name='admin_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:id>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),

    # Compras
    path('compras/', views.admin_compras, name='admin_compras'),

    # Usuarios
    path('usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('usuarios/<int:id>/editar-grupo/', views.editar_grupo_usuario, name='editar_grupo_usuario'),
    path('usuarios/<int:id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
]
