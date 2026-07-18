from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# En usuarios/views.py

def tienda_home(request):
    return render(request, 'tienda_home.html') # Nombre directo

def registro(request):
    # Aquí irá la lógica de tu formulario (arreglando el ImportError del formulario)
    return render(request, 'registro.html') # Nombre directo