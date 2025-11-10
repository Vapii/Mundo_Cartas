from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('noticias/', views.noticias, name='noticias'),
    path('noticias/<int:id>/', views.noticia_detail, name='detalle_noticia'),
]
