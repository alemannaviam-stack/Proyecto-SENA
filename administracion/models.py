from django.db import models


class DisenoSitio(models.Model):
    nombre_sitio = models.CharField(max_length=100, default="Nebula")
    logo = models.ImageField(upload_to='diseno/', blank=True, null=True)
    color_principal = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.nombre_sitio

    @classmethod
    def cargar(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj