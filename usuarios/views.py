from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from inventario.models import Producto


def tienda_home(request):
    productos = Producto.objects.filter(esta_activo=True)
    return render(request, 'tienda_home.html', {'productos': productos})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        messages.error(request, 'Correo o contraseña incorrectos.')
        return redirect('login')
    return render(request, 'login.html')


def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Ese correo ya está registrado.')
            return redirect('registro')

        user = User.objects.create_user(username=email, email=email, password=password, first_name=nombre)
        auth_login(request, user)
        return redirect('home')

    return render(request, 'login.html')