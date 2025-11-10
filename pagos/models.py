from django.db import models
from usuario.models import Usuario

class Pago(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    metodo = models.CharField(max_length=50)
    codigo_autorizacion = models.CharField(max_length=100)

    def __str__(self):
        return f'Pago de ${self.monto} por {self.usuario.username}'
