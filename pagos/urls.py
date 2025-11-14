from django.urls import path
from . import views

urlpatterns = [
    path('confirmar/', views.confirmar_pago, name='confirmar_pago'),
]
