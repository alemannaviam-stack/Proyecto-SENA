from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('inventario/', include('inventario.urls')),
    path('rastreo/', include('rastreo.urls')),  
    path('carrito/', include('carrito.urls')),
]


