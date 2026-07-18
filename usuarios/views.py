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
        return redirect('registro')
    return render(request, 'registro.html')


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User

def registro(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        
        # Creamos el usuario en la base de datos de manera segura
        nuevo_usuario = User.objects.create_user(username=usuario, email=correo, password=clave)
        
        # Iniciamos su sesión automáticamente
        login(request, nuevo_usuario)
        
        # Lo redirigimos a la tienda
        return redirect('tienda_home')
        
    return render(request, 'registro.html')