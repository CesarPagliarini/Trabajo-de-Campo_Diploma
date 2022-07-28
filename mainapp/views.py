from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from mainapp.models import Estadia
from .forms import RegisterForm, EstadiaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required             # Exporta la funcion que atentica previo a entrar a la url
from django.db.models import Q

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

# Crear/modificar estadia

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