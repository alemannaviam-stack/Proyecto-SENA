from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Envio, HistorialEstado

@login_required
def mi_rastreo(request, codigo):
    envio = get_object_or_404(Envio, numero_guia=codigo, cliente=request.user)
    return render(request, 'detalle_envio.html', {'envio': envio})

@login_required
def lista_mis_envios(request):
    envios = Envio.objects.filter(cliente=request.user).order_by('-fecha_creacion')
    return render(request, 'mis_envios.html', {'envios': envios})

@login_required
def actualizar_estado(request, envio_id):
    envio = get_object_or_404(Envio, id=envio_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        comentario = request.POST.get('comentario', '')
        envio.estado_actual = nuevo_estado
        envio.save()
        HistorialEstado.objects.create(envio=envio, estado=nuevo_estado, comentario=comentario)
        return redirect('dashboard_proveedor')
    return render(request, 'actualizar_estado.html', {'envio': envio})