from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Representa cada artículo físico en el inventario.
    """
    proveedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='articulos')

    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    esta_activo = models.BooleanField(default=True, help_text="Permite pausar la venta del producto sin eliminarlo")

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Stock(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='stock')
    cantidad = models.PositiveIntegerField(default=0)
    proveedor = models.ForeignKey('usuarios.Perfil', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'rol': 'proveedor'})

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"
    