from django.db import models
from mainapp.models import Estadia

# Create your models here.

class TipoRestaurante(models.Model):
    id_tipo_restaurante = models.AutoField(primary_key=True, editable=False, verbose_name='id_tipo_restaurante')
    descripcion = models.CharField(max_length=12, verbose_name='descripcion')
    
    class Meta:
        verbose_name = 'Tipo Restaurante'
        verbose_name_plural = 'Tipos Restaurantes'
        db_table = 'tipo_restaurante'
        
    def __str__(self):
        return f"{self.id_tipo_restaurante} - {self.descripcion}"



class Restaurante(models.Model):
    id_restaurante = models.AutoField(primary_key=True, editable=False, verbose_name='id_restaurante')
    nombre = models.CharField(max_length=25, verbose_name='nombre')
    tipo_restaurante = models.ForeignKey(TipoRestaurante, verbose_name='tipo_restaurante', on_delete=models.CASCADE)
    cant_mesas = models.IntegerField(verbose_name='cantidad_mesas')
    precio_base = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='precio_base')
    
    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
        db_table = 'restaurantes'
    
    def __str__(self):
        return f"{self.id_restaurante} - {self.nombre}"
    
    def get_id(self):
        return f"{self.id_restaurante}"
    
    
class EstadoReservaRestaurante(models.Model):
    id_estado = models.AutoField(primary_key=True, editable=False, verbose_name='id_estado')
    estado = models.CharField(max_length=12, verbose_name='estado')
    
    class Meta:
        verbose_name = 'Estado Reserva Restaurante'
        verbose_name_plural = 'Estados Reservas Restaurantes'
        db_table = 'estado_reserva_restaurante'
        
    def __str__(self):
        return f"{self.id_estado} - {self.estado}"
    

class TurnoReserva(models.Model):
    id_turno = models.AutoField(primary_key=True, editable=False, verbose_name='id_turno')
    horario = models.CharField(max_length=12, verbose_name='horario')
    
    class Meta:
        verbose_name = 'Turno Reserva'
        verbose_name_plural = 'Turnos Reservas'
        db_table = 'turnos_reservas'
        
    def __str__(self):
        return f"{self.id_turno} - {self.horario}"
    
    
class ReservaRestaurante(models.Model):
    id_reserva = models.AutoField(primary_key=True, editable=False, verbose_name='id_reserva')
    fecha_reserva = models.DateField(null=False, verbose_name='fecha_reserva')
    restaurante = models.ForeignKey(Restaurante, verbose_name='restaurante', on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoReservaRestaurante, verbose_name='estado', on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoReserva, verbose_name='turno', on_delete=models.CASCADE)
    estadia = models.ForeignKey(Estadia, verbose_name='estadia', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Reserva Restaurante'
        verbose_name_plural = 'Reservas Restaurantes'
        db_table = 'reservas_restaurantes'
        
    def __str__(self):
        return f"{self.id_reserva}"