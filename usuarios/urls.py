from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', views.tienda_home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]