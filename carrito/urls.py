# carrito/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. Ver Carrito
    path('', views.ver_carrito, name='ver_carrito'),
    
    # 2. Agregar al Carrito (Botón + en el carrito)
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    # 3. Eliminar UNA UNIDAD (Botón -)
    # Cambiado de 'carrito/eliminar_unidad/' a 'eliminar-unidad/' para una URL más limpia
    path('eliminar-unidad/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    
    # 4. ELIMINAR ÍTEM COMPLETO (Corrige el error NoReverseMatch)
    path('eliminar-completo/<int:item_id>/', views.eliminar_item_completo, name='eliminar_item_completo'),
]