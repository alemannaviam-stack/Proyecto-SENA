from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', views.tienda_home, name='tienda_home'),
    path('registro/', views.registro, name='registro'),
]