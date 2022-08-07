from dataclasses import fields
from random import choices
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django import forms
from .models import Estadia

class RegisterForm(UserCreationForm):
    class Meta:
        model = User                                                                           # Se basa en el model User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'groups', 'is_active']    # Los campos se pueden ver desde la tabla auth_user en la base de datos
        widgets = {
            'groups': forms.SelectMultiple(attrs = {
                'id': 'caja_grupos',
            }),
            'is_active': forms.CheckboxInput(attrs= {
                'default': 'checked',
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'label': 'Es administrador?',
            }),
        }
        
class RegistroModificacionForm(UserChangeForm):
    class Meta:
        model = User   
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'groups', 'is_active']
        widgets = {
            'groups': forms.SelectMultiple(attrs= {
                'id': 'caja_grupos',
            })
        }

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': forms.SelectMultiple(attrs = {
                'id': 'caja_permisos',
            }),
                
        }        
          
class EstadiaForm(forms.ModelForm):
    class Meta:
        model = Estadia
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.TextInput(attrs = {
                'type': 'date',
                'label': 'Fecha de inicio',
                'readonly': True,                                # Deja esta campo como de solo lectura
            }),
            'fecha_fin': forms.TextInput(attrs = {
                'type' : 'date',
                'label': 'Fecha de finalizacion',
                'readonly': True,                                # Deja esta campo como de solo lectura
            }),
            'huesped': forms.SelectMultiple(attrs = {
                'class': 'caja',
            }),
            'estado': forms.Select(attrs= {
                'class': 'caja2',
            }),
            'habitacion': forms.Select(attrs= {
                'class': 'caja2',
            }),
            'cantidad_dias': forms.TextInput(attrs= {
                'class': 'caja3',
                'readonly': True,                               # Deja esta campo como de solo lectura
            }),
            'penalizacion': forms.NumberInput(attrs= {
                'class': 'caja2',
                'readonly': True,                               # Deja esta campo como de solo lectura
            })
        }
 
        
class EstadiaFormInicial(forms.Form):
    id_estadia = forms.IntegerField(
       label = "Id de estadia",
       required=False,
       widget= forms.TextInput(
            attrs={
                'type': 'number',
                'readonly': True,
              }
        ),
    )
    
    fecha_inicio = forms.DateField(
        label = "Fecha ingreso",
        required=True,
        widget= forms.TextInput(
            attrs={
                'type': 'date',
              }
        ),
    )
    
    cantidad_dias = forms.IntegerField(
        label = "Cantidad de noches",
        required=True,
        widget= forms.NumberInput(
            attrs={
                'placeholder': 'Ingresa cantidad de noches',
              }
        ),
    )
    
    opciones_habitacion = [
        (1, 'Simple'),
        (2, 'Doble'),
        (3, 'Triple'),
        (4, 'Cuadruple'),
        (5, 'Estancia')
    ]
    
    tipo_habitacion = forms.IntegerField(
        label = "Seleccione tipo de habitacion",
        required = True,
        widget=forms.Select(
            choices = opciones_habitacion,
        )
    )
    
    

    