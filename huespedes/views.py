from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from huespedes.forms import FormHuesped                               # Importa el formulario FormHuesped
from huespedes.models import Huesped                                  # Importa el modelo Huesped
from django.contrib import messages
from django.contrib.auth.decorators import login_required             # Exporta la funcion que atentica previo a entrar a la url
from django.db.models import Q                                        # Objeto necesario para busquedas no simples.

# Create your views here.

# Crear huespedes
@login_required(login_url="login")                          # Requiere previa autenticación de usuario (login)
def formularioHuesped(request):
    
    if request.method == 'POST':                            # Recibe los datos del formulario por metodo POST.
        formulario = FormHuesped(request.POST)
    
        if formulario.is_valid():                           # Verifica que los datos sean validos.
            data_form = formulario.cleaned_data             
            
            dni = data_form['dni']                      # Asigna el contenido de cada campo del formulario a una variable local.
            nombre = data_form['nombre']
            apellido = data_form['apellido']
            fecha_nacimiento = data_form['fecha_nacimiento']
            pais = data_form['pais']
            direccion = data_form['direccion']
            telefono = data_form['telefono']
            mail = data_form['email']
            
            huesped = Huesped(                        # Crea un objeto de tipo Huesped.
                nombre = nombre,                      # Asigna el contenido de la variables anteriores a cada uno de los campos del objeto Huesped.
                apellido = apellido,
                dni = dni,
                fecha_nacimiento = fecha_nacimiento,
                pais = pais,
                direccion = direccion,
                telefono = telefono,
                mail = mail,
            )
            
            #return HttpResponse(f"Articulo creado: {huesped.nombre} {huesped.apellido} {huesped.dni} {huesped.pais} {huesped.direccion} {huesped.telefono} {huesped.mail}")   # Debug
        
            huesped.save()                                   # Guarda en la DB al objeto creado.
            messages.success(request, 'Registro exitoso')
            return redirect('listado_huespedes')             # Redirecciona al listado de Huespedes
        
        else:
            messages.success(request, 'Fracaso el registro')
    else:
        formulario = FormHuesped()
            
    return render(request, 'huespedes/alta_huesped.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de huesped',
        'cabecera': 'Alta de huesped'
    })


# Listar datos de huesped
@login_required(login_url="login")                          # Requiere previa autenticación de usuario (login)
def listado_huespedes(request):
    solicitud = request.POST.get('Buscar')
    huespedes = Huesped.objects.all()                       # Trae todas las instancias del objeto Huesped de la BD
    
    if solicitud:
        huespedes = Huesped.objects.filter(
            Q(dni__icontains = solicitud) | 
            Q(nombre__icontains = solicitud) |
            Q(apellido__icontains = solicitud)            # Q sirve para englobar la consulta y hace las veces de "or". icontains (%solicitud%)   
        ).distinct()                                      # Especifica que sean resultados diferentes
        
    return render(request, 'huespedes/listado_huespedes.html',{
        'huespedes': huespedes,
        'titulo': 'Huespedes',
        'cabecera': 'Listados de huespedes',
        'vacio': 'No se encontraron huespedes registrados',
    })
    
    
# Borar datos de huesped
@login_required(login_url="login")                                 # Requiere previa autenticación de usuario (login)    
def borrar_huesped(request, id):
    huesped = get_object_or_404(Huesped, pk=id)                    # Verifica que el id que le pase exista. Si es TRUE, trae los datos de la DB
    huesped.delete()                                               # Elimina el registro de la base de datos
    
    return redirect('listado_huespedes')


# Editar datos de huesped
@login_required(login_url="login")                          # Requiere previa autenticación de usuario (login)
def editar_huesped(request, id):
    huesped = get_object_or_404(Huesped, pk=id)             # Verifica que el id que le pase exista. Si es TRUE, trae los datos de la DB
      
    formulario = FormHuesped(initial={'dni': huesped.dni, 'nombre': huesped.nombre, 'apellido': huesped.apellido, 'fecha_nacimiento': huesped.fecha_nacimiento, 'pais': huesped.pais, 'direccion': huesped.direccion, 'telefono': huesped.telefono, 'email': huesped.mail})
        
    if request.method == 'POST':                            # Recibe los datos del formulario por metodo POST.
        formulario = FormHuesped(request.POST)
    
        if formulario.is_valid():                           # Verifica que los datos sean validos.
            data_form = formulario.cleaned_data             
           
            dni = data_form['dni']                      # Asigna el contenido de cada campo del formulario a una variable local.
            nombre = data_form['nombre']
            apellido = data_form['apellido']
            fecha_nacimiento = data_form['fecha_nacimiento']
            pais = data_form['pais']
            direccion = data_form['direccion']
            telefono = data_form['telefono']
            mail = data_form['email']

            huesped = Huesped(                        # Crea un objeto de tipo Huesped.
                nombre = nombre,                      # Asigna el contenido de la variables anteriores a cada uno de los campos del objeto Huesped.
                apellido = apellido,
                dni = dni,
                fecha_nacimiento = fecha_nacimiento,
                pais = pais,
                direccion = direccion,
                telefono = telefono,
                mail = mail,
            )
               
            huesped.save()                                   # Como el objeto ya existe en la base de datos, actualiza los datos.
            messages.success(request, 'Actualización exitoso')
            return redirect('listado_huespedes')             # Redireccion al listado de Huespedes
        
        else:
            messages.success(request, 'Fracaso la actualización')
             
    return render(request, 'huespedes/alta_huesped.html', {
        'form': formulario,
        'titulo': 'Formulario de modificación de huesped',
        'cabecera': 'Modificación de datos del huesped' 
    })
