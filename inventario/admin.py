from django.contrib import admin
from .models import Categoria, Producto, Stock

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'proveedor', 'precio', 'cantidad_disponible', 'esta_activo')
    list_filter = ('categoria', 'esta_activo')
    search_fields = ('nombre', 'marca')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'proveedor')