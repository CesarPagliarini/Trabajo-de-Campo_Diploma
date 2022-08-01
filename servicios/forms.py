from django import forms
from .models import ReservaServicio

class ReservaFormFinal(forms.ModelForm):
    class Meta:
        model = ReservaServicio
        fields = '__all__'
        widgets = {
            'fecha_reserva': forms.TextInput(attrs = {
                'type': 'date',
                'label': 'Fecha de inicio',
                'readonly': True,                                # Deja esta campo como de solo lectura
            }),
        }
        
class ReservaFormInicial(forms.Form):
    id_estadia = forms.IntegerField(
       label = "Id de estadia",
       required=False,
    )
    
    fecha_reserva = forms.DateField(
        label = "Fecha a reservar",
        required=True,
        widget= forms.TextInput(
            attrs={
                'type': 'date',
              }
        ),
    )
      
    opciones_servicios= [
        (1, 'Masajes'),
        (2, 'Spa'),
        (3, 'Lavadero'),
        (4, 'Tenis'),
        (5, 'Buceo'),
        (6, 'Bicicleta'),
        (7, 'Arqueria'),
    ]
    
    servicio = forms.IntegerField(
        label = "Seleccione el servicio",
        required = True,
        widget=forms.Select(
            choices = opciones_servicios,
        )
    )
