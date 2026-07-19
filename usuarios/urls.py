from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.tienda_home, name='tienda_home'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.tu_vista_de_perfil, name='perfil'),
    path('login/', views.login_view, name='login'), 
]