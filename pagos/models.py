# pagos/models.py

from django.db import models
from productos.models import Producto
from usuario.models import Usuario

class Pago(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.PositiveIntegerField()
    metodo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)
    codigo_autorizacion = models.CharField(max_length=100, default="SIN-CODIGO")
    buy_order = models.CharField(max_length=100, default="SIN-ORDEN")
    fecha = models.DateTimeField(auto_now_add=True)

class ItemCompra(models.Model):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
