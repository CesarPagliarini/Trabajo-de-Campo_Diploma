from django.shortcuts import render
from mainapp.models import Estadia
from huespedes.models import Huesped
from servicios.models import ReservaServicio
from django.db.models import Q

from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out
from django.utils import timezone
from auditoria.models import ActividadUsuario 

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

# Auditoria de accesos

@receiver(user_logged_in)
def register_user_login(sender, request, user, **kwargs):
    obj = ActividadUsuario.objects.create(usuario = user, login = timezone.now())
    request.session['user_activity_log_id'] = obj.id

@receiver(user_logged_out)
def register_user_logout(sender, request, user, **kwargs):
    ActividadUsuario.objects.filter(id = request.session['user_activity_log_id']).update(
        logout = timezone.now()
    )
    
def InformeAuditoriaAccesos(request):
    
    solicitud = request.POST.get('Buscar')
    accesos = ActividadUsuario.objects.all()
    campos = ['Id registro', 'Username', 'Fecha Login', 'Fecha Logout']
    
    if solicitud:
        accesos = ActividadUsuario.objects.filter(
            Q(user__username__icontains=solicitud) |
            Q(user__id__icontains=solicitud) 
        ).distinct()
        
    return render(request, 'auditorias/informe_accesos.html', {
        'titulo': 'Informe de accesos',
        'cabecera': 'accesos',
        'tabla': accesos,
        'campos': campos,
    })