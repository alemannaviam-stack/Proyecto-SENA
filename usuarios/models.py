from django.db import models
from django.contrib.auth.models import User

# Extensión del usuario para Clientes o Proveedores
class Perfil(models.Model):
    ROLES = (
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
        ('administrador', 'Administrador'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    # Solo aplica si es proveedor
    calificacion_positiva = models.IntegerField(default=0)
    calificacion_negativa = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)  # Para que el admin pueda "despedirlo" o desactivarlo

    def __str__(self):
        return f"{self.user.username} - {self.rol}"