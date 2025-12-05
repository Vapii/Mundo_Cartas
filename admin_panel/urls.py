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

    path("compras/", views.admin_compras, name="admin_compras"),
    path("detalle/<int:compra_id>/", views.detalle_compra, name="detail_compra"),

    # Usuarios
    path('usuario/crear/', views.crear_usuario_admin, name='crear_usuario'),
    path('usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('usuarios/<int:id>/editar-grupo/', views.editar_grupo_usuario, name='editar_grupo_usuario'),
    path('usuarios/<int:id>/toggle/', views.toggle_usuario, name='toggle_usuario'),
    path('usuarios/<int:id>/historial/', views.historial_compras_usuario, name='historial_compras_usuario'),


    # Noticias

    path('noticias/', views.listar_noticias, name='admin_noticias'),
    path('noticias/crear/', views.crear_noticia, name='crear_noticia'),
    path('noticias/<int:id>/editar/', views.editar_noticia, name='editar_noticia'),
    path('noticias/<int:id>/eliminar/', views.eliminar_noticia, name='eliminar_noticia'),

    # Banners

    path('banners/', views.listar_banners, name='admin_banners'),
    path('banners/crear/', views.crear_banner, name='crear_banner'),
    path('banners/<int:id>/eliminar/', views.eliminar_banner, name='eliminar_banner'),
    path('banners/<int:id>/toggle-activo/', views.toggle_activo_banner, name='toggle_activo_banner'),
    path('banners/<int:id>/editar/', views.editar_banner, name='editar_banner'),

    # Proveedores

    path('proveedores/', views.proveedores_list, name='admin_proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/<int:pk>/editar/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/<int:pk>/eliminar/', views.eliminar_proveedor, name='eliminar_proveedor'),

    # venta fisica

    path('ventas-fisicas/', views.admin_ventas_fisicas, name='admin_ventas_fisicas'),

]
