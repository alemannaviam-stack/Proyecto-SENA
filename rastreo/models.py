from django.db import models
from django.conf import settings
from inventario.models import Producto  # ajusta el nombre real de tu modelo


class Envio(models.Model):
    ESTADOS = [
        ('preparando', 'Preparando pedido'),
        ('en_camino', 'En camino'),
        ('en_reparto', 'En reparto local'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='envios')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado_actual = models.CharField(max_length=20, choices=ESTADOS, default='preparando')
    numero_guia = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Envío #{self.numero_guia} - {self.cliente}"


class HistorialEstado(models.Model):
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name='historial')
    estado = models.CharField(max_length=20, choices=Envio.ESTADOS)
    fecha = models.DateTimeField(auto_now_add=True)
    comentario = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f"{self.estado} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"