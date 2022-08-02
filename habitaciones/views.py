from django.shortcuts import render, HttpResponse
from habitaciones.models import Habitacion
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

@login_required(login_url="login")
def listado_habitaciones(request):
    solicitud = request.POST.get('Buscar')
    habitaciones = Habitacion.objects.all()
    if solicitud:
        habitaciones = Habitacion.objects.filter(Q(nro_habitacion__icontains=solicitud)| Q(tipo_habitacion__nombre__icontains=solicitud)| Q(estado__estado__icontains=solicitud)).distinct()                                              # Especifica que sean resultados diferentes

    #return HttpResponse(f"{habitaciones} - ")   # Debug
    return render(request, 'habitaciones/listado_habitaciones.html', {
        'habitaciones': habitaciones,
        'titulo': 'Habitaciones',
        'cabecera': 'Listados de habitaciones',
        'vacio': 'No se encontraron habitaciones que concuerden con los parametros ingresados',
        'boton': 'Regresar', 
    })
    
