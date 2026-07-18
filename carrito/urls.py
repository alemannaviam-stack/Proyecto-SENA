from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar/<int:item_id>/', views.quitar_item, name='quitar_item'),
    path('pagar/', views.confirmar_pago, name='confirmar_pago'),
]