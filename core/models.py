from django.db import models

class Noticia(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to="noticias", null=True, blank=True)

    def __str__(self):
        return self.titulo

from django.db import models

class Banner(models.Model):
    titulo = models.CharField(max_length=100, blank=True)
    imagen = models.ImageField(upload_to='banners/')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo or f"Banner {self.id}"

