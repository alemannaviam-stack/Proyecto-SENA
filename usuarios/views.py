from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.apps import apps

def tienda_home(request):
    Producto = apps.get_model('inventario', 'Producto') 
    
    productos = Producto.objects.filter(esta_activo=True)
    return render(request, 'tienda_home.html', {'productos': productos})

def login_view(request):
    if request.method == 'POST':
        correo_ingresado = request.POST.get('username') 
        clave_ingresada = request.POST.get('password')
        
        usuario_encontrado = User.objects.filter(email=correo_ingresado).first()
        
        if usuario_encontrado is not None:
            user = authenticate(request, username=usuario_encontrado.username, password=clave_ingresada)
            if user is not None:
                auth_login(request, user) # 🚀 Aquí guarda la sesión de verdad
                return redirect('tienda_home')
            else:
                return render(request, 'registro.html', {'error': 'Contraseña incorrecta.'})
        else:
            return render(request, 'registro.html', {'error': 'No existe la cuenta.'})
            
    return render(request, 'registro.html')

def registro(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        
        if User.objects.filter(username=usuario).exists() or User.objects.filter(email=correo).exists():
            return render(request, 'registro.html', {'error': 'El usuario o correo ya existen.'})
            
        nuevo_usuario = User.objects.create_user(username=usuario, email=correo, password=clave)
        
        auth_login(request, nuevo_usuario) # 🚀 Aquí guarda la sesión tras registrarse
        return redirect('tienda_home')
        
    return render(request, 'registro.html')

@login_required(login_url='login') # <-- Si no hay sesión, Django te mandará automáticamente a la ruta 'login'
def perfil(request):
    # Dejamos la vista apuntando a tu template real. 
    # Si aún no diseñas 'perfil.html' y te da error, puedes cambiar temporalmente 
    # la línea de abajo por: return redirect('tienda_home')
    return render(request, 'perfil.html')