from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Estadia

class RegisterForm(UserCreationForm):
    class Meta:
        model = User                                                                           # Se basa en el model User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff']    # Los campos se pueden ver desde la tabla auth_user en la base de datos
          
class EstadiaForm(forms.ModelForm):
    class Meta:
        model = Estadia
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.TextInput(attrs = {
                'type' : 'date',
                'label': 'Fecha de inicio',
            }),
            'fecha_fin': forms.TextInput(attrs = {
                'type' : 'date',
                'label': 'Fecha de finalizacion',
            }),
            'huesped': forms.SelectMultiple(attrs = {
                'class': 'caja',
            }),
        }