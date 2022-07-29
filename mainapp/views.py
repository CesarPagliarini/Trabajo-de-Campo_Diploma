from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from mainapp.models import Estadia
from habitaciones.models import Habitacion
from .forms import RegisterForm, EstadiaForm, EstadiaFormInicial
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required             # Exporta la funcion que atentica previo a entrar a la url
from django.db.models import Q                                        # Clase para operar con el ORM
from datetime import timedelta                                        # Necesario para operar con fecha


# Create your views here.

# Autenticacion de usuarios

def index(request):
    
    return render(request,'mainapp/index.html',{
        'title': 'Inicio'
    })


@login_required(login_url="login")                          # Requiere previa autenticación de usuario (login)
def register_page(request):
    
    register_form = RegisterForm()
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Te has registrado correctamente')
            
            return redirect('inicio')
        
    return render(request, 'users/register.html', {
        'title': 'Registro',
        'register_form': register_form
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
    

def logout_user(request):
    logout(request)
    return redirect('login')


# Estadias

# Prueba nuevo formulario

@login_required(login_url='login')
def alta_estadia_inicio(request):
    
    if request.method == 'POST':
        formulario = EstadiaFormInicial(request.POST)

        if formulario.is_valid():                           # Verifica que los datos sean validos.
            data_form = formulario.cleaned_data
            
            fecha_inicial = data_form['fecha_inicio']
            cantidad_dias = data_form['cantidad_dias']
            tipo_habitacion = data_form['tipo_habitacion']
            fecha_final = fecha_inicial + timedelta(cantidad_dias)
            
            habitacion_obj = Habitacion.objects.filter(tipo_habitacion = tipo_habitacion).exclude(Q(estadia__fecha_inicio__lte=fecha_final) & Q(estadia__fecha_inicio__gte=fecha_inicial)).exclude(Q(estadia__fecha_fin__gte=fecha_inicial) & Q(estadia__fecha_fin__lte=fecha_final)).exclude(Q(estadia__fecha_inicio__lte=fecha_inicial) & Q(estadia__fecha_fin__gte=fecha_final)).values('nro_habitacion').first()
            
            if habitacion_obj :
                habitacion = int(habitacion_obj['nro_habitacion'])                                               # Obtengo , del diccionario, el dato de la habitacion 
                #return HttpResponse(f"{fecha_inicial} - {fecha_final} -  {cantidad_dias} - {habitacion}")   # Debug
                return redirect('alta_estadia_final', cantidad_dias, habitacion)  
            else:
                messages.success(request, 'No se encontraron habitaciones disponibles')
        
    else:
        formulario = EstadiaFormInicial()
            
    return render(request, 'estadias/alta_estadia.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de estadia - Paso 1',
        'cabecera': 'Alta de estadia'
    })
            
@login_required(login_url='login') 
def alta_estadia_final(request, cantidad_dias, habitacion):
    
    formulario = EstadiaForm(initial={'cantidad_dias': cantidad_dias,
                                      'habitacion': habitacion,
                                      })

    #return HttpResponse(f"{cantidad_dias} - {habitacion}")   # Debug
    if request.method == 'POST':
        formulario = EstadiaForm(request.POST)
        
        if formulario.is_valid():
            estadia = formulario.save()
            messages.success(request, 'Registro exitoso')
            return redirect('listado_estadias')       
        else:
            messages.success(request, 'Fracaso el registro')
    else:
        messages.success(request, 'Fracaso la registracion')
            
    return render(request, 'estadias/alta_estadia.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de estadia',
        'cabecera': 'Alta Estadia'
    })           
            
            
#Crear/modificar estadia

@login_required(login_url='login')
def formulario_estadia(request, id=None):
    try:
        estadia = Estadia.objects.get(pk=id)
    except Estadia.DoesNotExist:
        estadia = None  
    
    if request.method == 'POST':
        formulario = EstadiaForm(request.POST, instance=estadia)
        
        if formulario.is_valid():
            estadia = formulario.save()
            messages.success(request, 'Registro exitoso')
            return redirect('listado_estadias')       
        else:
            messages.success(request, 'Fracaso el registro')         
    else:
        formulario = EstadiaForm(instance=estadia)
        
    return render(request, 'estadias/alta_estadia.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de estadia',
        'cabecera': 'Alta Estadia'
    })
   
    
# Listar datos de estadia
@login_required(login_url="login")                          
def listado_estadias(request):
    #solicitud = request.POST.get('Buscar')
    estadias = Estadia.objects.all()                      
    
    #if solicitud:
    #    estadias = Estadia.objects.filter(
    #        Q(dni__icontains = solicitud) | 
    #        Q(nombre__icontains = solicitud) |
    #        Q(apellido__icontains = solicitud)            
    #    ).distinct()                                      # Especifica que sean resultados diferentes
        
    return render(request, 'estadias/listado_estadias.html',{
        'estadias': estadias,
        'titulo': 'Estadias',
        'cabecera': 'Listados de estadias',
        'vacio': 'No se encontraron estadias registradas',
    })
    
# Borar datos de estadia
@login_required(login_url="login")                                 # Requiere previa autenticación de usuario (login)    
def borrar_estadia(request, id):
    estadia = get_object_or_404(Estadia, pk=id)                    # Verifica que el id que le pase exista. Si es TRUE, trae los datos de la DB
    estadia.delete()                                               # Elimina el registro de la base de datos
    
    return redirect('listado_estadias')