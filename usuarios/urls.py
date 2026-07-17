from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', auth_views.LoginView.as_view(template_name='tienda_home.html'), name='home'),
    #path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('registro/', views.registro_usuario, name='registro'),
    #path('redireccionar/', views.redireccionar_por_rol, name='redireccionar_por_rol'),
]