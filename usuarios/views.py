from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventario.models import Producto


def tienda_home(request):
    productos = Producto.objects.filter(esta_activo=True)
    return render(request, 'tienda_home.html', {'productos': productos})


def registro(request):
    return render(request, 'registro.html')