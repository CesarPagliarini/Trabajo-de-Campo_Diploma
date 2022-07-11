from unittest.util import _MAX_LENGTH
from django import forms                                 # Importa el paquetes de forms desde la librería de Django
from django.core import validators                       # Sirve para realizar una gran variedad de validaciones

class FormHuesped(forms.Form):

    dni = forms.IntegerField(
        label = "Dni",
        required=True,
        widget= forms.NumberInput(
            attrs={
                'placeholder': 'Introduzca el dni',
            }
        ),
        validators=[
            validators.MinLengthValidator(100000, 'El valor es demasiado pequeño'),     # Valida la longitud mínima del campo
            validators.RegexValidator('^[0-9] *$', message='Solo se pueden ingresar numeros')   # Valida que solo se ingresen números
        ]
    )
    
    nombre = forms.CharField(                               
        label = "Nombre",
        max_length= 25,
        required=True,
        widget= forms.TextInput(
            attrs={
                'placeholder': 'Introduzca el nombre',
            }
        )  ,
        validators=[
            validators.MinLengthValidator(3, 'El nombre es demasiado corto'),
            validators.RegexValidator('^[A-Za-zñ ]*$', message='El nombre esta mal formado')            # Valida que solo se ingresen letras,espacios y la letra ñ
        ]
    )
    
    apellido = forms.CharField(                                    
        label = "Apellido",
        max_length= 25,
        required=True,
        widget= forms.TextInput(
            attrs={
                'placeholder': 'Introduzca el apellido',
            }
        )  ,
        validators=[
            validators.MinLengthValidator(2, 'El apellido es demasiado corto'),
            validators.RegexValidator('^[A-Za-zñ ]*$', message='El apellido esta mal formado')            
        ]
    )
    
    direccion = forms.CharField(                                    
        label = "Direccion",
        max_length= 25,
        required=True,
        widget= forms.TextInput(
            attrs={
                'placeholder': 'Introduzca la dirección',
            }
        )  ,
        validators=[
            validators.MinLengthValidator(6, 'La dirección es demasiado corta'),
            validators.RegexValidator('^[A-Za-z0-9ñ ]*$', message='El titulo esta mal formado')            # Valida que solo se ingresen números,letras,espacios y la letra ñ
        ]
    )
    
    telefono = forms.CharField(                                    
        label = "Telefono",
        max_length= 14,
        required=True,
        widget= forms.TextInput(
            attrs={
                'placeholder': 'Introduzca el telefono sin espacios',
            }
        )  ,
        validators=[
            validators.MinLengthValidator(7, 'El teléfono es demasiado corta'),                            # Longitud mínima de caracteres
            validators.MaxLengthValidator(14, 'Se excede la cantidad máxima de dígitos'),                  # Longitud máxima de caracteres
            validators.RegexValidator('^(\+)?[0-9]*$', message='El teléfono esta mal formado'),            # Valida que solo se ingresen números y el signo + (solo lo acepta al inicio).   
        ]
    )
    
    email = forms.EmailField(                                    
        label = "Email",
        max_length= 40,
        required=True,
        widget= forms.TextInput(
            attrs={
                'placeholder': 'Introduzca la direccion de correo',
            }
        )  ,
        validators=[
            validators.MinLengthValidator(6, 'La direccion es demasiado corta'),
            validators.RegexValidator('^[A-Za-z0-9ñ@._-]*$', message='El titulo esta mal formateado')     # Valida que solo se ingresen números,letras,caracter ñ, @ , puntos y guiones _ -
        ]
    )
    
    pais = forms.CharField(                                    
        label = "Pais",
        max_length= 25,
        required=True,
        widget= forms.TextInput(
            attrs={
                'placeholder': 'Introduzca el pais',
            }
        )  ,
        validators=[
            validators.MinLengthValidator(4, 'El pais es demasiado corto'),
            validators.RegexValidator('^[A-Za-zñ ]*$', message='El pais esta mal formado')            # Valida que solo se ingresen letras,espacios y la letra ñ
        ]
    )
    
    fecha_nacimiento = forms.DateField(                                    
        label = "Fecha de Nacimiento",
        required=True,
        widget= forms.DateInput(
            attrs={
                'placeholder': 'Introduzca la fecha de nacimiento',
            }
        )  ,
        validators=[
            validators.MinLengthValidator(4, 'La fecha no respeta el formato'),
            validators.RegexValidator('^[0-9\/]*$', message='La ciudad esta mal formateada')            # Valida que solo se ingresen números y el caracter separador /
        ]
    )