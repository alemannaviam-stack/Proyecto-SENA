from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps  

def es_administrador(user):
    return user.is_authenticated and hasattr(user, 'perfil') and user.perfil.rol == 'ADMIN'


# ==========================================
# dashboard

@login_required(login_url='usuarios:login')
def admin_dashboard(request):
    if not es_administrador(request.user):
        return redirect('usuarios:tienda_home')
        
    # 🌟 Traemos el modelo Perfil dinámicamente de la app 'usuarios' sin usar import
    Perfil = apps.get_model('usuarios', 'Perfil')
    
    # Conseguir los proveedores que están esperando aprobación
    proveedores_pendientes = Perfil.objects.filter(rol='PROVEEDOR', usuario__is_active=False) 
    
    context = {
        'proveedores_pendientes': proveedores_pendientes
    }
    return render(request, 'administracion/dashboard.html', context)


# ==========================================
# aprovar proveedores

@login_required(login_url='usuarios:login')
def aprobar_proveedor(request, perfil_id):
    if not es_administrador(request.user):
        return redirect('usuarios:tienda_home')
        
    # 🌟 Traemos el modelo Perfil dinámicamente sin usar import
    Perfil = apps.get_model('usuarios', 'Perfil')
        
    perfil = get_object_or_404(Perfil, id=perfil_id)
    
    # Activar el usuario proveedor en el sistema
    user_proveedor = perfil.usuario
    user_proveedor.is_active = True
    user_proveedor.save()
    
    return redirect('administracion:dashboard')


# ==========================================
# gestion/ productos

@login_required(login_url='usuarios:login')
def gestion_diseno_productos(request):
    if not es_administrador(request.user):
        return redirect('usuarios:tienda_home')
        
    # 🌟 Traemos el modelo Producto dinámicamente de tu app de 'carrito' (o 'inventario')
    Producto = apps.get_model('carrito', 'Producto') 
    
    productos = Producto.objects.all()
    
    return render(request, 'administracion/gestion_diseno.html', {'productos': productos})