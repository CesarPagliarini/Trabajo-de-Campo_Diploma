from tabnanny import verbose
from django.db import models

# Create your models here.

class TipoHabitacion(models.Model):
    id_tipo_habitacion = models.AutoField(primary_key=True, editable=False, verbose_name='id_tipo_habitacion')
    nombre = models.CharField(max_length=12, verbose_name='nombre')
    capacidad = models.IntegerField(verbose_name='capacidad')
    superficie = models.IntegerField(verbose_name='superficie')
    cantidad_ambientes = models.IntegerField(verbose_name='cantidad_ambientes')
    cantidad_banos = models.IntegerField(verbose_name='cantidad_banos')
    precio_por_noche = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='precio_por_noche')
    
    class Meta:
        verbose_name = 'Tipo de habitacion'
        verbose_name_plural = 'Tipos de habitaciones'
        db_table = 'tipo_habitaciones' 
        
    def __str__(self):
        return f"{self.id_tipo_habitacion} - {self.nombre}"                     # En el administrador va a mostrar: 1 - Simple (ejemplo) - Seccion TipoHabitacion

class EstadoHabitacion(models.Model):
    nro_estado = models.AutoField(primary_key=True, editable=False, verbose_name='nro_estado')
    estado = models.CharField(max_length=10, verbose_name='estado')
    
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        db_table = 'estados_habitacion'
        
    def __str__(self):
        return f"{self.nro_estado} - {self.estado}"
    
    
class Habitacion(models.Model):
    nro_habitacion = models.AutoField(primary_key=True, editable=False, verbose_name='nro_habitacion')
    estado = models.ForeignKey(EstadoHabitacion, verbose_name='estado', on_delete=models.CASCADE)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, verbose_name='tipo_habitacion', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Habitacion'
        verbose_name_plural = 'Habitaciones'
        db_table = 'habitaciones' 
        
    def __str__(self):
        return f"{self.nro_habitacion}"
    

    

    
