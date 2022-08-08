from django.shortcuts import render
from mainapp.models import Estadia
from huespedes.models import Huesped
from servicios.models import ReservaServicio

# Create your views here.

def InformeAuditoriaEstadias(request):
    estadias = Estadia.objects.all()
    
    return render(request, 'auditorias/informe.html', {
        'titulo': 'Informe de estadias',
        'cabecera': 'Estadias',
        'tabla': estadias,
    })
