from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Huesped(models.Model):
    dni_huesped = models.IntegerField(validators=[MinValueValidator(1000000)], verbose_name='Dni')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=255, verbose_name='Apellido')
    fecha_nacimiento = models.DateField(verbose_name='Fecha_nacimiento')
    pais = models.CharField(max_length=20, verbose_name='Pais')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    user = models.ForeignKey(User, editable=False, verbose_name='Usuario', on_delete=models.CASCADE, default=2)
    
    class Meta:
        verbose_name = 'Huesped'
        verbose_name_plural = 'Huespedes'
        db_table = 'huespedes' 
        
    def __str__(self):
        return self.nombre