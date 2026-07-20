from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('proveedores/aprobar/<int:perfil_id>/', views.aprobar_proveedor, name='aprobar_proveedor'),
    path('productos/editar-diseno/', views.gestion_diseno_productos, name='gestion_diseno'),
]