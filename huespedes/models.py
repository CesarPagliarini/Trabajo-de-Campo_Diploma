from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Huesped(models.Model):
    dni = models.CharField(primary_key=True, max_length=9, verbose_name='Dni')
    nombre = models.CharField(max_length=25, verbose_name='Nombre')
    apellido = models.CharField(max_length=25, verbose_name='Apellido')
    fecha_nacimiento = models.DateField(verbose_name='Fecha_nacimiento')
    pais = models.CharField(max_length=25, verbose_name='Pais')
    direccion = models.CharField(max_length=25, verbose_name='Direccion', default=None)
    telefono = models.CharField(max_length=14, verbose_name='Telefono', default=None)
    mail = models.EmailField(max_length=40, verbose_name='Email', default=None)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    user = models.ForeignKey(User, editable=False, verbose_name='Usuario', on_delete=models.CASCADE, default=2)
    
    class Meta:
        verbose_name = 'Huesped'
        verbose_name_plural = 'Huespedes'
        db_table = 'huespedes' 
        
    def __str__(self):
        return f"{self.dni} - {self.nombre} {self.apellido}"