from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', auth_views.LoginView.as_view(template_name='tienda_home.html'), name='home'),
]