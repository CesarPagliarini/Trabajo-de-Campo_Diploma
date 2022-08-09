from dataclasses import dataclass
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from habitaciones.models import TipoHabitacion, Habitacion
from servicios.models import ReservaServicio, Servicio
from mainapp.models import Estadia
from restaurantes.models import Restaurante, ReservaRestaurante
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.

def ReporteServicios(request):
    
    service = []
    now = datetime.now()
    hoy = now.date()
    servicios = Servicio.objects.all()
    try:
        for servicio in servicios:
            dato = servicio.get_codigo()
            cantidad_reserva = ReservaServicio.objects.filter(servicio=dato).count()
            if cantidad_reserva == None:
                cantidad_reserva = '0'
            
            service.append(cantidad_reserva)
        #return HttpResponse(f"{service}")   # Debug
    except:
        pass

    return render (request, 'reportes/reporte servicios.html', {
        'service': service,
    }) 
    

def ReporteRestaurantes(request):
    contador = 0
    reservas = []
    
    now = datetime.now()
    hoy = now.date()
    restaurantes = Restaurante.objects.all()
    cantidad_total_reservas = ReservaRestaurante.objects.all().count()
    try:
        for resto in restaurantes:
            contador = contador + 1
            dato = resto.get_id()
            nombre = resto.getNombre()
            cantidad_reserva = ReservaRestaurante.objects.filter(restaurante=dato).count()
            if cantidad_reserva == None:
                cantidad_reserva = '0'
            
            porcentaje = float((cantidad_reserva / cantidad_total_reservas) * 100)
            #elemento['name'] = nombre
            #elemento['y'] = porcentaje
            reservas.append(porcentaje)
    except:
        pass
        #return HttpResponse(f"{p}")   # Debug
    return render (request, 'reportes/reporte restaurantes.html', {
        'porcentaje': porcentaje,
    }) 
