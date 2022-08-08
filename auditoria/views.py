from django.shortcuts import render
from mainapp.models import Estadia
from huespedes.models import Huesped
from servicios.models import ReservaServicio
from django.db.models import Q

# Create your views here.

def InformeAuditoriaEstadias(request):
    
    solicitud = request.POST.get('Buscar')
    estadias = Estadia.objects.all()
    campos = ['Id estadia', 'Fecha inicio', 'Cantidad de dias', 'Creado por', 'Creado', 'Editado por', 'Editado']
    
    if solicitud:
        estadias = Estadia.objects.filter(
            Q(user__username__icontains=solicitud) |
            Q(user_update__username__icontains=solicitud) |
            Q(id_estadia__icontains=solicitud)
        ).distinct()
        
    return render(request, 'auditorias/informe_estadias.html', {
        'titulo': 'Informe de estadias',
        'cabecera': 'Estadias',
        'tabla': estadias,
        'campos': campos,
    })
    
def InformeAuditoriaServicios(request):
    
    solicitud = request.POST.get('Buscar')
    reservas = ReservaServicio.objects.all()
    campos = ['Id reserva', 'Fecha reserva', 'Servicio', 'Creado por', 'Creado', 'Editado por', 'Editado']
    
    if solicitud:
        estadias = ReservaServicio.objects.filter(
            Q(user__username__icontains=solicitud) |
            Q(user_update__username__icontains=solicitud) |
            Q(id_reserva__icontains=solicitud)
        ).distinct()
        
    return render(request, 'auditorias/informe_servicios.html', {
        'titulo': 'Informe de Reservas de Servicios',
        'cabecera': 'servicios',
        'tabla': reservas,
        'campos': campos,
    })

