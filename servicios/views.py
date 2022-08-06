from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from mainapp.models import Estadia
from servicios.models import ReservaServicio, Servicio, EstadoReserva
from .forms import ReservaFormInicial, ReservaFormFinal
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime

# Create your views here.

# Lista Reservas


@login_required(login_url="login")
def listado_reservas_servicios(request):
    solicitud = request.POST.get('Buscar')
    reservas = ReservaServicio.objects.all()
    if solicitud:
        reservas = ReservaServicio.objects.filter(
            Q(estadia__id_estadia__icontains=solicitud) |
            Q(id_reserva__icontains=solicitud) |
            Q(estadia__habitacion__nro_habitacion__icontains=solicitud)
        ).distinct()                                              # Especifica que sean resultados diferentes

    # return HttpResponse(f"{estadias.id_estadia} - {estadias.fecha_inicio} - {estadias.fecha_fin} - {estadias.cantidad_dias} - {estadias.nro_habitacion} - {estadias.fecha_inicio}")   # Debug
    return render(request, 'servicios/listado_reservas_servicios.html', {
        'reservas': reservas,
        'titulo': 'Reservas Servicio',
        'cabecera': 'Listados de reservas de servicios',
        'vacio': 'No se encontraron reservas registradas',
    })

# Borar datos de reserva

# Requiere previa autenticación de usuario (login)
@login_required(login_url="login")
def borrar_reserva_servicio(request, id):
    # Verifica que el id que le pase exista. Si es TRUE, trae los datos de la DB
    reserva = get_object_or_404(ReservaServicio, pk=id)
    # Elimina el registro de la base de datos
    reserva.delete()

    return redirect('listado_reservas_servicios')

# Alta reserva Servicio


@login_required(login_url='login')
def alta_reserva_inicio(request):

    mensaje = 'vacio'
    now = datetime.now()
    
    if request.method == 'POST':
        formulario = ReservaFormInicial(request.POST)

        # Verifica que los datos sean validos.
        if formulario.is_valid():
            data_form = formulario.cleaned_data

            id_estadia = data_form['id_estadia']
            fecha_reserva = data_form['fecha_reserva']
            id_servicio = data_form['servicio']

            try:
                estadia = Estadia.objects.get(pk=id_estadia)
            except Estadia.DoesNotExist:
                estadia = None

            if estadia != None:
                if estadia.estado.estado == 'Iniciada':
                    if estadia.fecha_fin > fecha_reserva:
                        if fecha_reserva > now.date():
                            servicio_obj = Servicio.objects.get(pk=id_servicio)
                            cant_reservas = ReservaServicio.objects.filter(Q(servicio__id_servicio=id_servicio) & Q(
                                fecha_reserva=fecha_reserva) & Q(estado__estado='Pendiente')).count()

                            if cant_reservas < servicio_obj.maximo_diario:
                                dia = fecha_reserva.day
                                mes = fecha_reserva.month
                                anio = fecha_reserva.year
                                # return HttpResponse(f"{id_estadia} - {id_servicio}")   # Debug
                                return redirect('alta_reserva_servicio_final', id_estadia, dia, mes, anio, id_servicio)
                            else:
                                mensaje = 'Se alcanzo la cantidad máxima de lugares disponibles'
                        else:
                            mensaje = 'La fecha selecciona es anterior  a la fecha actual'
                    else:
                        mensaje = 'La fecha de reserva del servicio debe ser anterior a la finalización de la estadia'
                else:
                    mensaje = 'La estadia no inicio o ya finalizo'
            else:
                mensaje = 'El codigo ingresado no pertenece a un estadia registrada'
    else:
        formulario = ReservaFormInicial()

    return render(request, 'servicios/alta_reserva_servicio.html', {
        'form': formulario,
        'titulo': 'Formulario alta de reserva de servicio',
        'cabecera': 'Alta de reserva de servicio',
        'mensaje': mensaje,
        'boton': 'Continuar'
    })


@login_required(login_url='login')
def alta_reserva_servicio_final(request, id_estadia, dia, mes, anio, id_servicio):

    fecha_reserva = date(anio, mes, dia)

    formulario = ReservaFormFinal(initial={'estadia': id_estadia,
                                           'fecha_reserva': fecha_reserva,
                                           'servicio': int(id_servicio),
                                           'estado': 1,                                  # Opcion de estado 'Pendiente'
                                           })

    # return HttpResponse(f"{cantidad_dias} - {habitacion}")   # Debug
    if request.method == 'POST':
        formulario = ReservaFormFinal(request.POST)

        if formulario.is_valid():
            reserva = formulario.save(commit=False)
            # Agrega el usuario que esta manipulando el formulario
            reserva.user = request.user
            reserva.save()
            messages.success(request, 'Registro exitoso')
            return redirect('listado_reservas_servicios')
        else:
            messages.success(request, 'Fracaso el registro')

    return render(request, 'servicios/alta_reserva_servicio.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de estadia',
        'cabecera': 'Alta Estadia',
        'boton': 'Guardar',
    })

# Editar Reserva
@login_required(login_url='login')
def editar_reserva_servicio(request, id, estado):

    mensaje = ''
    reserva = get_object_or_404(ReservaServicio, pk=id)

    formulario = ReservaFormInicial(initial={'id_reserva': reserva.id_reserva , 'id_estadia': reserva.estadia.id_estadia, 'fecha_reserva': reserva.fecha_reserva, 'servicio': reserva.servicio})
    if estado == 1:
        if request.method == 'POST':
            formulario = ReservaFormInicial(request.POST)

            # Verifica que los datos sean validos.
            if formulario.is_valid():
                data_form = formulario.cleaned_data

                fecha_reserva = data_form['fecha_reserva']
                servicio = data_form['servicio']

                servicio_obj = Servicio.objects.get(pk=int(servicio))
                cant_reservas = ReservaServicio.objects.filter(Q(servicio__id_servicio=servicio) & Q(
                                fecha_reserva=fecha_reserva) & Q(estado__estado='Pendiente')).count()

                if cant_reservas < servicio_obj.maximo_diario:
                    cod_servicio = servicio_obj.get_codigo()
                    return redirect('editar_reserva_servicio_final', reserva.id_reserva, cod_servicio)
                    #return HttpResponse(f"{cod_servicio}")   # Debug
                else:
                    mensaje = 'Se alcanzo la cantidad maximo diaria para este servicio'
    else:
        mensaje = 'La estadia ya fue tomada o se encuentra vencida, no puede modificarse'
                        
    return render(request, 'servicios/alta_reserva_servicio.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de estadia - Paso 1',
        'cabecera': 'Alta de estadia',
        'mensaje': mensaje,
        'boton': 'Continuar'
    })
    
@login_required(login_url='login')
def editar_reserva_servicio_final(request, id, servicio):
    
    mensaje = 'vacio'
    try:
        reserva = ReservaServicio.objects.get(pk=id)
        servicio_obj = Servicio.objects.get(pk=servicio)
    except ReservaServicio.DoesNotExist:
        reserva = None
    
    if request.method == 'POST':
        formulario = ReservaFormFinal(request.POST, instance=reserva)

        if formulario.is_valid():
            reserva = formulario.save()
            reserva.servicio = servicio_obj                                     # Actualizo el campo de la servicio
            #reserva.user_update = request.user
            reserva.save()

            return redirect('listado_reservas_servicios')
        else:
            messages.success(request, 'Fracaso la edicion')
    else:
        formulario = ReservaFormFinal(instance=reserva)

    return render(request, 'servicios/alta_reserva_servicio.html', {
        'form': formulario,
        'titulo': 'Edicion de reserva de servicio',
        'cabecera': 'Modificacion de reserva',
        'mensaje': mensaje,
        'boton': 'Guardar',
    })

# Tomar reserva
@login_required(login_url="login")
def tomar_reserva_servicio(request, id, estado):
    
    mensaje = 'vacio'
    try:
        reserva = ReservaServicio.objects.get(pk=id)
    except Estadia.DoesNotExist:
        reserva = None
    
    now = datetime.now()
    
    if estado == 1:    
        if reserva.fecha_reserva <  now.date():
            mensaje = 'La reserva ya no es valida'
            reserva.estado = EstadoReserva.objects.get(pk='4')
            reserva.save(commit=False) 
            #reserva.user_update = request.user
            reserva.save()
        elif now.date() < reserva.fecha_reserva:
            mensaje = f'Reserva no valida para el dia de la fecha. Regresar el dia {reserva.fecha_reserva}'
        else:
            reserva.estado = EstadoReserva.objects.get(pk='2')
            reserva.user = request.user
            reserva.save()
            return redirect('listado_reservas_servicios')
    else:
        mensaje = 'El estado de la reserva debe ser Pendiente'
            
    return render(request, 'servicios/alta_reserva_servicio.html', {
        'titulo': 'Toma de reserva',
        'cabecera': 'Modificacion de estado de la reserva',
        'mensaje': mensaje
    })