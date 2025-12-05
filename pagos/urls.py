from django.urls import path
from . import views

urlpatterns = [
    path("webpay/commit/", views.commit_pago, name="commit_pago"),
    path("iniciar/", views.iniciar_pago, name="iniciar_pago"),
    path("confirmar/", views.confirmar_pago, name="confirmar_pago"),
]
