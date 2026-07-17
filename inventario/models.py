from django.db import models
from usuarios.models import Perfil  # Buscar juntar los modelos

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_module='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Stock(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='stock')
    cantidad = models.PositiveIntegerField(default=0)
    proveedor = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol': 'proveedor'})

    def __str__(self):
        return f"{self.producto.nombre} - Stock: {self.cantidad}"