from django.shortcuts import render
from huespedes.forms import FormHuesped                               # Importa el formulario FormHuesped
from huespedes.models import Huesped                                  # Importa el modelo Huesped
from django.contrib import messages
from django.contrib.auth.decorators import login_required           # exporta la funcion que atentica previo a entrar a la url

# Create your views here.

@login_required(login_url="login")                          # Requiere previa autenticación de usuario (login)
def formularioHuesped(request):

    if request.method == 'POST':                            # Recibe los datos del formulario por metodo POST.
        formulario = FormHuesped(request.POST)
    
        if formulario.is_valid():                           # Verifica que los datos sean validos.
            data_form = formulario.cleaned_data             
            
            dni = data_form.get('dni')                      # Asigna el contenido de cada campo del formulario a una variable local.
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
            
            huesped.save()                              # Guarda en la DB al objeto creado.
            messages.success(request, 'Registro exitoso')
            #return render('listar_huespedes')          # Redirecciona al listado de Huespedes
        
        else:
            messages.success(request, 'Fracaso el registro')
    else:
        formulario = FormHuesped()
            
    return render(request, 'huespedes/alta_huesped.html', {
        'form': formulario,
        'titulo': 'Formulario de alta de huesped',
        'cabecera': 'Alta de huesped'
    })

