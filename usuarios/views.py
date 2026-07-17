from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def redireccionar_por_rol(request):
    rol_usuario = request.user.perfil.rol
    
    if rol_usuario == 'ADMIN':
        return redirect('dashboard_admin')  # Apunta a la vista del admin
    elif rol_usuario == 'PROVEEDOR':
        return redirect('dashboard_proveedor')  # Apunta al panel de inventario
    else:
        return redirect('tienda_home')  # Apunta a la tienda de los clientes