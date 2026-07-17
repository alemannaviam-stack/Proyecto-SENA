from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class RegistroUsuarioForm(forms.ModelForm):
    rol = forms.ChoiceField(choices=Perfil.ROLES, label="¿Cómo te vas a registrar?")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono / Celular")
    direccion = forms.CharField(max_length=255, required=False, label="Dirección de envío/bodega")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    confirmar_password = forms.CharField(widget=forms.PasswordInput(), label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario (Login)',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password != confirmar_password:
            raise forms.ValidationError("¡Las contraseñas no coinciden!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            perfil = user.perfil
            perfil.rol = self.cleaned_data.get('rol')
            perfil.telefono = self.cleaned_data.get('telefono')
            perfil.direccion = self.cleaned_data.get('direccion')
            perfil.save()
        return user