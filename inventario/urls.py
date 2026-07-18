from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_proveedor, name='dashboard'),
    path('agregar/', views.agregar_producto, name='agregar'),
]
