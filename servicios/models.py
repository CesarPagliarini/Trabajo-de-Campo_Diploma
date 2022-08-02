from django.db import models
from django.contrib.auth.models import User
from mainapp.models import Estadia

# Create your models here.

class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True, editable=False, verbose_name='id_servicio')
    servicio = models.CharField(max_length=12, verbose_name='servicio')
    precio = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='precio')
    accesorios = models.CharField(max_length=50, verbose_name='accesorios')
    maximo_diario = models.IntegerField(verbose_name='maximo_diario')
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        db_table = 'servicios'
        
    def __str__(self):
        return f"{self.id_servicio} - {self.servicio}"
    
    def get_codigo(self):
        return f"{self.id_servicio}"


class EstadoReserva(models.Model):
    nro_estado = models.AutoField(primary_key=True, editable=False, verbose_name='nro_estado')
    estado = models.CharField(max_length=10, verbose_name='estado')
    
    class Meta:
        verbose_name = 'Estado Reserva'
        verbose_name_plural = 'Estados Reservas'
        db_table = 'estados_reserva'
        
    def __str__(self):
        return f"{self.nro_estado} - {self.estado}"
    
           
class ReservaServicio(models.Model):
    id_reserva = models.AutoField(primary_key=True, editable=False, verbose_name='id_reserva')
    fecha_reserva = models.DateField(null=False, verbose_name='fecha_reserva')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='modificado')
    estado = models.ForeignKey(EstadoReserva, verbose_name='estado', on_delete=models.CASCADE)
    estadia = models.ForeignKey(Estadia, verbose_name='estadia', on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, verbose_name='servicio', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, editable=False, verbose_name='usuario', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Reserva Servicio'
        verbose_name_plural = 'Reservas Servicios'
        db_table = 'reservas_servicio' 
        ordering = ['id_reserva']
        
    def __str__(self):
        return f"{self.id_reserva} - {self.estado.estado} - {self.fecha_reserva}"	
