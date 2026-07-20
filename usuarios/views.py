from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from administracion.models import DisenoSitio
from django.apps import apps

# ==========================================
# 1. TIENDA HOME (VISTA PÚBLICA)
# ==========================================
def tienda_home(request):
    Producto = apps.get_model('inventario', 'Producto') 
    productos = Producto.objects.filter(esta_activo=True)
    return render(request, 'tienda_home.html', {'productos': productos})


# ==========================================
# 2. INICIO DE SESIÓN (LOGIN)
# ==========================================
def login_view(request):
    if request.method == 'POST':
        correo_ingresado = request.POST.get('username')
        clave_ingresada = request.POST.get('password')

        usuario_encontrado = User.objects.filter(email=correo_ingresado).first()

        if usuario_encontrado is not None:
            user = authenticate(request, username=usuario_encontrado.username, password=clave_ingresada)
            if user is not None:
                auth_login(request, user)
                return redirect_por_rol(user)
            else:
                return render(request, 'registro.html', {'error': 'Contraseña incorrecta.'})
        else:
            return render(request, 'registro.html', {'error': 'No existe la cuenta.'})

    return render(request, 'registro.html')


# ==========================================
# 3. REDIRECCIÓN DINÁMICA POR ROL
# ==========================================
def redirect_por_rol(user):
    rol = user.perfil.rol

    if rol == 'PROVEEDOR':
        # 🌟 CORREGIDO: Apunta a la función 'dashboard' de esta app con su namespace
        return redirect('usuarios:dashboard')
    elif rol == 'ADMIN':
        # 🌟 CORREGIDO: Redirige al namespace de la app independiente 'administracion'
        return redirect('administracion:dashboard')
    else:  # CLIENTE
        return redirect('usuarios:tienda_home')


# ==========================================
# 4. REGISTRO DE USUARIOS NUEVOS
# ==========================================
def registro(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        
        if User.objects.filter(username=usuario).exists() or User.objects.filter(email=correo).exists():
            return render(request, 'registro.html', {'error': 'El usuario o correo ya existen.'})
            
        nuevo_usuario = User.objects.create_user(username=usuario, email=correo, password=clave)
        
        auth_login(request, nuevo_usuario)
        return redirect('usuarios:tienda_home')
        
    return render(request, 'registro.html')


# ==========================================
# 5. PERFIL DE USUARIO
# ==========================================
@login_required(login_url='usuarios:login')  # 🌟 CORREGIDO: Namespace del login
def perfil(request):
    return render(request, 'perfil.html')


# ==========================================
# 6. DASHBOARD / PANEL DEL PROVEEDOR
# ==========================================
@login_required(login_url='usuarios:login')
def dashboard(request):
    if request.user.perfil.rol != 'PROVEEDOR':
        return redirect('usuarios:tienda_home')
        
    return render(request, 'dashboard_proveedor.html')

# ==========================================
# 7. PÁGINA PRINCIPAL DE LA TIENDA
# ==========================================
def tienda_home(request):
    productos = Producto.objects.all()
 
    diseno = DisenoSitio.cargar()
 
    return render(request, 'usuarios/pagina_principal.html', {
        'productos': productos,
        'diseno': diseno,  
    })
 