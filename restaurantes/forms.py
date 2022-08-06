from urllib import request
from django import forms
from .models import ReservaRestaurante

class ReservaRestauranteFormFinal(forms.ModelForm):
    class Meta:
        model = ReservaRestaurante
        fields = '__all__'
        widgets = {
            'fecha_reserva': forms.TextInput(attrs = {
                'type': 'date',
                'label': 'Fecha Reserva',
                'readonly': True,                                # Deja esta campo como de solo lectura
            }),
            
            'restaurante': forms.Select(attrs= {
                'class': 'caja',
            }),
            
            'estado': forms.Select(attrs= {
                'class': 'caja2',
            }),
                        
            'estadia': forms.Select(attrs= {
                'class': 'caja2',
            }),
            
            'turno': forms.Select(attrs= {
                'class': 'caja2',
            })
        }
        
        
class ReservaRestauranteFormInicial(forms.Form):
    id_reserva = forms.IntegerField(
       label = "Id de reserva",
       required=False,
       widget= forms.TextInput(
            attrs={
                'type': 'number',
                'readonly': True,
              }
        ),
    )
    
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
      
    opciones_restaurantes= [
        (1, 'Bendita Costilla'),
        (2, 'Pasion por las Brasas'),
        (3, 'Pujol'),
        (4, 'Narisawa'),
        (5, 'Attica'),
        (6, 'Biko'),
        (7, 'Nahm'),
        (8, 'Combal.Zero'),
        (9, 'Piazza Duomo'),
    ]
    
    restaurante = forms.IntegerField(
        label = "Seleccione el restaurante que desee",
        required = True,
        widget=forms.Select(
            choices = opciones_restaurantes,
            attrs={
                'class': 'caja2',
            })
        )
    
    opciones_horarios= [
        (1, '19 hs'),
        (2, '19:45 hs'),
        (3, '20:30 hs'),
        (4, '21:15 hs'),
        (5, '22 hs'),
        (6, '22:45 hs'),
        (7, '23:30 hs'),
    ]
    
    turno = forms.CharField(
        label = "Seleccione el horario deseado",
        required = True,
        widget = forms.Select(
            choices= opciones_horarios,   
        )
    )
