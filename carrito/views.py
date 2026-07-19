import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.apps import apps # 🚀 IMPORTANTE: Importamos el buscador de apps de Django
from .models import Carrito, ItemCarrito

# Quitamos por completo los imports problemáticos de aquí arriba para limpiar VS Code

@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(cliente=request.user)
    return render(request, 'carrito.html', {'carrito': carrito})


@login_required
def agregar_al_carrito(request, producto_id):
    # 🚀 Traemos el modelo Producto dinámicamente de la app 'inventario'
    Producto = apps.get_model('inventario', 'Producto')
    
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, _ = Carrito.objects.get_or_create(cliente=request.user)

    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        item.cantidad += 1
        item.save()

    messages.success(request, f'{producto.nombre} añadido al carrito.')
    return redirect('ver_carrito')


@login_required
def quitar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__cliente=request.user)
    item.delete()
    return redirect('ver_carrito')


@login_required
def confirmar_pago(request):
    carrito, _ = Carrito.objects.get_or_create(cliente=request.user)
    items = carrito.items.all()

    if not items:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('ver_carrito')

    # 🚀 Traemos los modelos de rastreo dinámicamente de la app 'rastreo'
    Envio = apps.get_model('rastreo', 'Envio')
    HistorialEstado = apps.get_model('rastreo', 'HistorialEstado')

    envios_creados = []
    for item in items:
        numero_guia = str(uuid.uuid4())[:8].upper()
        envio = Envio.objects.create(
            cliente=request.user,
            producto=item.producto,
            numero_guia=numero_guia,
        )
        HistorialEstado.objects.create(envio=envio, estado='preparando', comentario='Pago confirmado (simulado)')
        envios_creados.append(envio)

    items.delete()  # vacía el carrito
    messages.success(request, f'¡Pago exitoso! Se generaron {len(envios_creados)} envío(s).')
    return redirect('rastreo:mis_envios')