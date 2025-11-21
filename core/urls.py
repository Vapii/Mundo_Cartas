from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('noticias/', views.noticias, name='noticias'),
    path('noticias/todas/', views.todas_las_noticias, name='todas_noticias'),

]
