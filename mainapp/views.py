from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from mainapp.models import Estadia, EstadoEstadia, Reglamento
from habitaciones.models import Habitacion, EstadoHabitacion
from .forms import RegisterForm, EstadiaForm, EstadiaFormInicial, RegistroModificacionForm, GrupoForm
from django.contrib.auth import authenticate, login, logout
# Exporta la funcion que atentica previo a entrar a la url
from django.contrib.auth.decorators import login_required
# Clase para operar con el ORM
from django.db.models import Q
# Necesario para operar con fecha
from datetime import datetime, timedelta, date
from django.contrib.auth.models import User, Group

# Create your views here.

# Autenticacion de usuarios

def index(request):

    return render(request, 'mainapp/index.html', {
        'title': 'Inicio'
    })


# Requiere previa autenticación de usuario (login)
@login_required(login_url="login")
def register_page(request, id=None):

    try:
        usuario = User.objects.get(pk=id)
        registro = RegistroModificacionForm
    except User.DoesNotExist:
        usuario = None
        registro = RegisterForm
        
    if request.method == 'POST':
        register_form = registro(request.POST, instance=usuario)

        if register_form.is_valid():
            usuario = register_form.save()
            messages.success(request, 'Te has registrado correctamente')

            return redirect('listado_usuarios')

    else:
        register_form = registro(instance=usuario)
        
    return render(request, 'users/register.html', {
        'title': 'Registro',
        'register_form': register_form
    })

# Listar datos de usuarios
@login_required(login_url="login")
def listado_usuarios(request):
    solicitud = request.POST.get('Buscar')
    usuarios = User.objects.all()
    if solicitud:
        usuarios = User.objects.filter(username=solicitud).distinct()              # Especifica que sean resultados diferentes

    return render(request, 'users/listado_usuarios.html', {
        'usuarios': usuarios,
        'titulo': 'Usuarios',
        'cabecera': 'Listados de usuarios',
        'vacio': 'No se encontraro ningun usuario registradas con ese username',
    })
    
    
def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.warning(request, 'No te has podido identificar')

    return render(request, 'users/login.html', {
        'title': 'Identificate',
    })

@login_required(login_url="login")                  # Requiere previa autenticación de usuario (login)
def borrar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)     # Verifica que el id que le pase exista. Si es TRUE, trae los datos de la DB
    usuario.delete()                                # Elimina el registro de la base de datos

    return redirect('listado_usuarios')


def logout_user(request):
    logout(request)
    return redirect('login')


#Grupos

@login_required(login_url="login")
def alta_grupo(request, id=None):

    try:
        grupo = Group.objects.get(pk=id)
    except Group.DoesNotExist:
        grupo = None
        
    if request.method == 'POST':
        formulario = GrupoForm(request.POST, instance=grupo)

        if formulario.is_valid():
            grupo = formulario.save()
            messages.success(request, 'Te has registrado correctamente')

            return redirect('listado_grupos')

    else:
        formulario = GrupoForm(instance=grupo)
        
    return render(request, 'users/alta_grupo.html', {
        'title': 'Registro',
        'formulario': formulario
    })
    
    
# Listar datos de grupos
@login_required(login_url="login")
def listado_grupos(request):
    solicitud = request.POST.get('Buscar')
    grupos = Group.objects.all()
    if solicitud:
        grupos = Group.objects.filter(name=solicitud).distinct()              # Especifica que sean resultados diferentes

    return render(request, 'users/listado_grupos.html', {
        'grupos': grupos,
        'titulo': 'Grupos',
        'cabecera': 'Listados de Grupos',
        'vacio': 'No se encontraron grupos registradas con ese nombre',
    })

# Estadias

@login_required(login_url='login')
def alta_estadia_inicio(request):

    mensaje = 'vacio'
    if request.method == 'POST':
        formulario = EstadiaFormInicial(request.POST)

        # Verifica que los datos sean validos.
        if formulario.is_valid():
            data_form = formulario.cleaned_data

            fecha_inicial = data_form['fecha_inicio']
            cantidad_dias = data_form['cantidad_dias']
            tipo_habitacion = data_form['tipo_habitacion']
            fecha_final = fecha_inicial + timedelta(cantidad_dias)

            habitacion_obj = Habitacion.objects.filter(tipo_habitacion=tipo_habitacion).exclude(Q(estadia__fecha_inicio__lte=fecha_final) & Q(estadia__fecha_inicio__gte=fecha_inicial)).exclude(
                Q(estadia__fecha_fin__gte=fecha_inicial) & Q(estadia__fecha_fin__lte=fecha_final)).exclude(Q(estadia__fecha_inicio__lte=fecha_inicial) & Q(estadia__fecha_fin__gte=fecha_final)).values('nro_habitacion').first()

            if habitacion_obj:
                # Obtengo , del diccionario, el dato de la habitacion
                habitacion = int(habitacion_obj['nro_habitacion'])

                # Conversion fecha inicio de date a integer para pasarla como parametro
                dia_inicio = fecha_inicial.day
                mes_inicio = fecha_inicial.month
                anio_inicio = fecha_inicial.year

                dia_fin = fecha_final.day
                mes_fin = fecha_final.month
                anio_fin = fecha_final.year

                # return HttpResponse(f"{dia} - {mes} - {anio} - {cantidad_dias} - {habitacion}")   # Debug
                return redirect('alta_estadia_final', dia_inicio, mes_inicio, anio_inicio, dia_fin, mes_fin, anio_fin, cantidad_dias, habitacion)
            else:
                mensaje = 'No se encontraron habitaciones disponibles'

    else:
        formulario = EstadiaFormInicial()

    return render(request, 'estadias/alta_estadia.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de estadia - Paso 1',
        'cabecera': 'Alta de estadia',
        'mensaje': mensaje,
        'boton': 'Continuar',
    })


@login_required(login_url='login')
def alta_estadia_final(request, dia_inicio, mes_inicio, anio_inicio, dia_fin, mes_fin, anio_fin, cantidad_dias, habitacion):

    mensaje = ''
    fecha_inicio = date(anio_inicio, mes_inicio, dia_inicio)
    fecha_fin = date(anio_fin, mes_fin, dia_fin)

    formulario = EstadiaForm(initial={'cantidad_dias': cantidad_dias,
                                      'habitacion': habitacion,
                                      'fecha_inicio': fecha_inicio,
                                      'fecha_fin': fecha_fin,
                                      'estado': 1,                                  # Opcion de estado 'Reservada'
                                      })
    now = datetime.now()
    if fecha_inicio >= now.date():
        # return HttpResponse(f"{cantidad_dias} - {habitacion}")   # Debug
        if request.method == 'POST':
            formulario = EstadiaForm(request.POST)

            if formulario.is_valid():
                estadia = formulario.save(commit=False)
                #estadia.user = request.user
                estadia.save()
                messages.success(request, 'Registro exitoso')
                return redirect('listado_estadias')
            else:
                messages.success(request, 'Fracaso el registro')
    else:
        mensaje = 'La fecha de inicio es anterior a la fecha actual'
        
    return render(request, 'estadias/alta_estadia.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de estadia',
        'cabecera': 'Alta Estadia',
        'boton': 'Guardar',
        'mensaje': mensaje,
    })


# Listar datos de estadia
@login_required(login_url="login")
def listado_estadias(request):
    solicitud = request.POST.get('Buscar')
    estadias = Estadia.objects.all()
    if solicitud:
        estadias = Estadia.objects.filter(
            Q(huesped__dni__icontains=solicitud) |
            Q(id_estadia__icontains=solicitud) |
            Q(habitacion__nro_habitacion__icontains=solicitud)
        ).distinct()                                              # Especifica que sean resultados diferentes

    # return HttpResponse(f"{estadias.id_estadia} - {estadias.fecha_inicio} - {estadias.fecha_fin} - {estadias.cantidad_dias} - {estadias.nro_habitacion} - {estadias.fecha_inicio}")   # Debug
    return render(request, 'estadias/listado_estadias.html', {
        'estadias': estadias,
        'titulo': 'Estadias',
        'cabecera': 'Listados de estadias',
        'vacio': 'No se encontraron estadias registradas',
    })


# Editar estadia
def editar_estadia(request, id, estado):

    mensaje = ''
    estadia = get_object_or_404(Estadia, pk=id)

    formulario = EstadiaFormInicial(initial={'id_estadia': estadia.id_estadia, 'fecha_inicio': estadia.fecha_inicio,
                                    'cantidad_dias': estadia.cantidad_dias, 'tipo_habitacion': estadia.habitacion.tipo_habitacion.id_tipo_habitacion})
    if estado == 1:
        if request.method == 'POST':
            formulario = EstadiaFormInicial(request.POST)

            # Verifica que los datos sean validos.
            if formulario.is_valid():
                data_form = formulario.cleaned_data

                fecha_inicial = data_form['fecha_inicio']
                tipo_habitacion = data_form['tipo_habitacion']
                fecha_final = estadia.fecha_fin

                habitacion_obj = Habitacion.objects.filter(tipo_habitacion=tipo_habitacion).exclude(Q(estadia__fecha_inicio__lte=fecha_final) & Q(estadia__fecha_inicio__gte=fecha_inicial)).exclude(
                    Q(estadia__fecha_fin__gte=fecha_inicial) & Q(estadia__fecha_fin__lte=fecha_final)).exclude(Q(estadia__fecha_inicio__lte=fecha_inicial) & Q(estadia__fecha_fin__gte=fecha_final)).values('nro_habitacion').first()

                if habitacion_obj:
                    # Obtengo , del diccionario, el dato de la habitacion
                    habitacion = int(habitacion_obj['nro_habitacion'])

                    #return HttpResponse(f"{estadia.id_estadia} - {habitacion}")   # Debug
                    return redirect('editar_estadia_final', estadia.id_estadia, habitacion)
                else:
                    mensaje = 'No se encontraron habitaciones disponibles'
    else:
        mensaje = 'La estadia ya fue tomada, fue finalizada o se encuentra vencida, no puede ser modificada'
        
    return render(request, 'estadias/alta_estadia.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de estadia - Paso 1',
        'cabecera': 'Alta de estadia',
        'boton': 'Continuar',
        'mensaje': mensaje
    })


@login_required(login_url='login')
def editar_estadia_final(request, id, habitacion):
    
    mensaje = 'vacio'
    try:
        estadia = Estadia.objects.get(pk=id)
        habitacion_obj = Habitacion.objects.get(pk=habitacion)
    except Estadia.DoesNotExist:
        estadia = None
        messages.success(request, 'No existe la estadia')
    
    if request.method == 'POST':
        formulario = EstadiaForm(request.POST, instance=estadia)

        if formulario.is_valid():
            estadia = formulario.save(commit=False)
            estadia.habitacion = habitacion_obj                                     # Actualizo el campo de la habitacion
            #estadia.user_update = request.user
            estadia.save()

            return redirect('listado_estadias')
        else:
            messages.success(request, 'Fracaso la edicion')
    else:
        formulario = EstadiaForm(instance=estadia)

    return render(request, 'estadias/alta_estadia.html', {
        'form': formulario,
        'titulo': 'Edicion de estadia',
        'cabecera': 'Modificacion de estadia',
        'mensaje': mensaje,
        'boton': 'Guardar'
    })

# Check-in / Check-out


@login_required(login_url="login")
def checkin_checkout_estadia(request, id, accion, estado):

    mensaje = 'vacio'
    respuesta = ''
    
    estadia = Estadia.objects.get(pk=id)        # Busca la instancia de estadia correpondiente
    habitacion = Habitacion.objects.get(pk=estadia.habitacion.nro_habitacion)   # Obtiene la instancia de habitacion asociada

    if accion == 'in':
        if estado == 1:
            estado_estadia = EstadoEstadia.objects.get(pk='2')
            estado_habitacion = EstadoHabitacion.objects.get(pk='3')
            respuesta = 'ok'
        else:
            mensaje = 'La estadia debe poseer estado reservada'
    elif accion == 'out':
        if estado == 2:
            estado_estadia = EstadoEstadia.objects.get(pk='3')
            estado_habitacion = EstadoHabitacion.objects.get(pk='1')
            respuesta = 'ok'
            now = datetime.now()
            if estadia.fecha_fin > now.date():
                penalizacion = Reglamento.get_instancia().retiro_anticipado
                estadia.penalizacion = penalizacion
                #return HttpResponse(f"{penalizacion}")   # Debug
                estadia.fecha_fin = now.date()
        else:
            mensaje = 'La estadia debe poseer estado tomada'
            
    if respuesta == 'ok':
        estadia.estado = estado_estadia          # Asigna el valor al campo 'estado' del objeto    
        habitacion.estado = estado_habitacion
        #estadia.user_update = request.user
        estadia.save()                           # Guarda el objeto en la base de datos
        habitacion.save()
        return redirect('listado_estadias')
    else:
        return render(request, 'estadias/alta_estadia.html', {
        'titulo': 'Registro checkin/out',
        'cabecera': 'Modificacion de estadia',
        'mensaje': mensaje
    })


# Borar datos de estadia
@login_required(login_url="login")                  # Requiere previa autenticación de usuario (login)
def borrar_estadia(request, id):
    estadia = get_object_or_404(Estadia, pk=id)     # Verifica que el id que le pase exista. Si es TRUE, trae los datos de la DB
    estadia.delete()                                    # Elimina el registro de la base de datos

    return redirect('listado_estadias')



# Auditoria

def auditoria(request):
    
    return 
    
