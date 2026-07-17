from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm

@login_required
def dashboard_proveedor(request):
    if request.user.perfil.rol != 'PROVEEDOR':
        return redirect('login')
        
    # Filtra los productos de este proveedor
    mis_productos = Producto.objects.filter(proveedor=request.user)
    # Renderiza directo al HTML global sin subcarpetas
    return render(request, 'dashboard_proveedor.html', {'inventario': mis_productos})


@login_required
def agregar_producto(request):
    if request.user.perfil.rol != 'PROVEEDOR':
        return redirect('login')

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.proveedor = request.user
            producto.save()
            messages.success(request, '¡Producto añadido con éxito al inventario!')
            return redirect('dashboard_proveedor')
    else:
        form = ProductoForm()
        
    return render(request, 'agregar_producto.html', {'form': form})