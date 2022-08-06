from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from mainapp.models import Estadia
from restaurantes.models import Restaurante, ReservaRestaurante, EstadoReservaRestaurante, TurnoReserva
from .forms import ReservaRestauranteFormInicial, ReservaRestauranteFormFinal
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime

# Create your views here.

# Lista Reservas

@login_required(login_url="login")
def listado_reservas_restaurantes(request):
    solicitud = request.POST.get('Buscar')
    reservas = ReservaRestaurante.objects.all()
    if solicitud:
        reservas = ReservaRestaurante.objects.filter(
            Q(estadia__id_estadia__icontains=solicitud) |
            Q(id_reserva__icontains=solicitud) |
            Q(reserva__restaurante__nombre__icontains=solicitud)
        ).distinct()                                              # Especifica que sean resultados diferentes

    # return HttpResponse(f"{estadias.id_estadia} - {estadias.fecha_inicio} - {estadias.fecha_fin} - {estadias.cantidad_dias} - {estadias.nro_habitacion} - {estadias.fecha_inicio}")   # Debug
    return render(request, 'restaurantes/listado_reservas_restaurantes.html', {
        'reservas': reservas,
        'titulo': 'Reservas Restaurante',
        'cabecera': 'Listados de reservas de restaurantes',
        'vacio': 'No se encontraron reservas registradas',
    })
    

# Muestra los datos de un restaurante y la cantidad de mesas libres para hoy
@login_required(login_url="login")
def detalles_restaurante(request, id):

    fecha = datetime.now()
    hoy = fecha.date()
    
    restaurante = Restaurante.objects.get(pk=id)
    reservas = ReservaRestaurante.objects.filter(fecha_reserva = hoy).count()           # Cuenta cantidad de reservas para hoy
    cant_turnos = TurnoReserva.objects.all().count()
    
    return render(request, 'restaurantes/detalles.html', {
        'restaurante': restaurante,
        'reservas': reservas,
        'cant_turnos': cant_turnos,
        'titulo': 'Detalles del Restaurante',
        'cabecera': 'Detalles del Restaurante',
    })
    
# Borar datos de reserva

# Requiere previa autenticación de usuario (login)
@login_required(login_url="login")
def borrar_reserva_restaurante(request, id):

    mensaje = 'vacio'
    reserva = get_object_or_404(ReservaRestaurante, pk=id)     # Verifica que el id que le pase exista. Si es TRUE, trae los datos de la DB
    if reserva:
        fecha = datetime.now()
        hoy = fecha.date()
        if reserva.fecha_reserva > hoy:
            
            reserva.delete()        # Elimina el registro de la base de datos
            return redirect('listado_reservas_restaurantes')
        else:
            mensaje = 'Las reservas se cancelan con NO menos de 24 hs de anticipación'
    else:
        mensaje = 'La reserva no existe'
        
    return render(request, 'restaurantes/listado_reservas_restaurantes.html', {
        'titulo': 'Cacelacion de reservas de restaurantes',
        'cabecera': 'Cancelacion de reservas',
        'mensaje': mensaje,
    })


# Alta reserva Servicio

@login_required(login_url='login')
def alta_reserva_restaurante_inicio(request):

    mensaje = 'vacio'
    now = datetime.now()
    
    if request.method == 'POST':
        formulario = ReservaRestauranteFormInicial(request.POST)

        # Verifica que los datos sean validos.
        if formulario.is_valid():
            data_form = formulario.cleaned_data

            id_estadia = data_form['id_estadia']
            fecha_reserva = data_form['fecha_reserva']
            id_restaurante = data_form['restaurante']
            turno = data_form['turno']

            try:
                estadia = Estadia.objects.get(pk=id_estadia)
            except Estadia.DoesNotExist:
                estadia = None

            if estadia != None:
                if estadia.estado.estado == 'Iniciada':
                    if estadia.fecha_fin > fecha_reserva:                                   # Verifica que la reserva este dentro de la estadia
                        if fecha_reserva >= now.date():                                     # Evita que haga una reserva para ayer (por ejemplo)
                            restaurante_obj = Restaurante.objects.get(pk=id_restaurante)    # Busca la instancia de restaurante correspondiente
                            cant_reservas = ReservaRestaurante.objects.filter(Q(restaurante__id_restaurante=id_restaurante) & Q(
                                fecha_reserva=fecha_reserva) & Q(estado__estado='Pendiente') & Q(turno__id_turno=turno)).count()

                            if cant_reservas < restaurante_obj.cant_mesas:
                                dia = fecha_reserva.day
                                mes = fecha_reserva.month
                                anio = fecha_reserva.year
                                # return HttpResponse(f"{id_estadia} - {id_servicio}")   # Debug
                                return redirect('alta_reserva_restaurante_final', id_estadia, dia, mes, anio, id_restaurante, turno)
                            else:
                                mensaje = 'Se alcanzo la cantidad máxima de lugares disponibles para el horario seleccionado'
                        else:
                            mensaje = 'La fecha selecciona es anterior  a la fecha actual'
                    else:
                        mensaje = 'La fecha de reserva del servicio debe ser anterior a la finalización de la estadia'
                else:
                    mensaje = 'La estadia no inicio o ya finalizo'
            else:
                mensaje = 'El código ingresado no pertenece a un estadia registrada'
    else:
        formulario = ReservaRestauranteFormInicial()

    return render(request, 'restaurantes/alta_reserva_restaurante.html', {
        'form': formulario,
        'titulo': 'Formulario alta de reserva de restaurante',
        'cabecera': 'Alta de reserva de restaurante',
        'mensaje': mensaje,
        'boton': 'Continuar'
    })
    
    
@login_required(login_url='login')
def alta_reserva_restaurante_final(request, id_estadia, dia, mes, anio, id_restaurante, horario):
    mensaje = 'vacio'
    fecha_reserva = date(anio, mes, dia)

    formulario = ReservaRestauranteFormFinal(initial={'estadia': id_estadia,
                                           'fecha_reserva': fecha_reserva,
                                           'restaurante': int(id_restaurante),
                                           'estado': 1,                                  # Opcion de estado 'Reservada'
                                           'turno': horario,
                                           })

    if request.method == 'POST':
        formulario = ReservaRestauranteFormFinal(request.POST)
        
        if formulario.is_valid():
            reserva = formulario.save(commit=False)
            # Agrega el usuario que esta manipulando el formulario
            reserva.user = request.user
            reserva.save()
            messages.success(request, 'Registro exitoso')
            return redirect('listado_reservas_restaurantes')
        else:
            mensaje = 'Fracaso el registro'

    return render(request, 'restaurantes/alta_reserva_restaurante.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de reserva',
        'cabecera': 'Alta Reserva restaurante',
        'boton': 'Guardar',
        'mensaje': mensaje
    })
    
    # Editar Reserva
@login_required(login_url='login')
def editar_reserva_restaurante(request, id, estado):

    mensaje = ''
    reserva = get_object_or_404(ReservaRestaurante, pk=id)

    formulario = ReservaRestauranteFormInicial(initial={'id_reserva': reserva.id_reserva , 'id_estadia': reserva.estadia.id_estadia, 'fecha_reserva': reserva.fecha_reserva, 'restaurante': reserva.restaurante.id_restaurante, 'turno': reserva.turno.id_turno})
    if estado == 1:
        if request.method == 'POST':
            formulario = ReservaRestauranteFormInicial(request.POST)

            # Verifica que los datos sean validos.
            if formulario.is_valid():
                data_form = formulario.cleaned_data

                fecha_reserva = data_form['fecha_reserva']
                restaurante = data_form['restaurante']
                turno = data_form['turno']

                restaurante_obj = Restaurante.objects.get(pk=int(restaurante))
                cant_reservas = ReservaRestaurante.objects.filter(Q(restaurante__id_restaurante=restaurante) & Q(
                                fecha_reserva=fecha_reserva) & Q(estado__estado='Pendiente') & Q(turno__id_turno=turno)).count()

                if cant_reservas < restaurante_obj.cant_mesas:
                    cod_restaurante = restaurante_obj.get_id()
                    return redirect('editar_reserva_restaurante_final', reserva.id_reserva, cod_restaurante)
                    #return HttpResponse(f"{cod_servicio}")   # Debug
                else:
                    mensaje = 'Se alcanzo la cantidad maximo diaria para este servicio'
    else:
        mensaje = 'La estadia ya fue tomada o se encuentra vencida, no puede modificarse'
                        
    return render(request, 'restaurantes/alta_reserva_restaurante.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de reservas Restaurante - Paso 1',
        'cabecera': 'Alta de reserva',
        'mensaje': mensaje,
        'boton': 'Continuar'
    })
    
@login_required(login_url='login')
def editar_reserva_restaurante_final(request, id, restaurante):
    
    mensaje = 'vacio'
    try:
        reserva = ReservaRestaurante.objects.get(pk=id)
        restaurante_obj = Restaurante.objects.get(pk=restaurante)
    except ReservaRestaurante.DoesNotExist:
        reserva = None
    
    if request.method == 'POST':
        formulario = ReservaRestauranteFormFinal(request.POST, instance=reserva)

        if formulario.is_valid():
            reserva = formulario.save()
            reserva.restaurante = restaurante_obj                                     # Actualizo el campo de la servicio
            #reserva.user_update = request.user
            reserva.save()

            return redirect('listado_reservas_restaurantes')
        else:
            messages.success(request, 'Fracaso la edicion')
    else:
        formulario = ReservaRestauranteFormFinal(instance=reserva)

    return render(request, 'restaurantes/alta_reserva_restaurante.html', {
        'form': formulario,
        'titulo': 'Edicion de reserva de restaurante',
        'cabecera': 'Modificacion de reserva',
        'mensaje': mensaje,
        'boton': 'Guardar',
    })
    
# Tomar reserva
@login_required(login_url="login")
def tomar_reserva_restaurante(request, id, estado):
    
    mensaje = 'vacio'
    try:
        reserva = ReservaRestaurante.objects.get(pk=id)
    except Estadia.DoesNotExist:
        reserva = None
    
    now = datetime.now()
    
    if estado == 1:    
        if reserva.fecha_reserva <  now.date():
            mensaje = 'La reserva ya no es valida'
            reserva.estado = EstadoReservaRestaurante.objects.get(pk='4')
            reserva.save(commit=False) 
            #reserva.user_update = request.user
            reserva.save()
        elif now.date() < reserva.fecha_reserva:
            mensaje = f'Reserva no valida para el dia de la fecha. Regresar el dia {reserva.fecha_reserva}'
        else:
            reserva.estado = EstadoReservaRestaurante.objects.get(pk='2')
            reserva.user = request.user
            reserva.save()
            return redirect('listado_reservas_restaurantes')
    else:
        mensaje = 'El estado de la reserva debe ser Pendiente'
            
    return render(request, 'restaurantes/alta_reserva_restaurante.html', {
        'titulo': 'Toma de reserva',
        'cabecera': 'Modificacion de estado de la reserva',
        'mensaje': mensaje
    })