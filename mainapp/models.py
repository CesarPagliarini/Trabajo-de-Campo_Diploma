from django.db import models
from django.contrib.auth.models import User
from pkg_resources import require
from huespedes.models import Huesped
from habitaciones.models import Habitacion

# Create your models here.

# Posible aplicacion de Singleton
class Descuentos(models.Model):
    id_descuento = models.AutoField(primary_key=True, unique=True, null=False, editable=False, verbose_name='id_descuento')
    descripcion = models.CharField(max_length=12, null=False, verbose_name='descripcion')                          # Ejemplo: 25%
    estado = models.CharField(max_length=12, null=False, verbose_name='estado')                                    # Disponible, Usado
    multiplicador = models.DecimalField(max_digits=4, decimal_places=3, null=False, verbose_name='multiplicador')   # Ejemplo: 0.125
    
    class Meta:
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
        db_table = 'descuentos' 
        ordering = ['id_descuento']
        
    def __str__(self):
        return f"{self.id_descuento} - {self.descripcion}"
    

class Estadia(models.Model):
    id_estadia = models.AutoField(primary_key=True, editable=False, verbose_name='id_estadia')
    estado = models.CharField(max_length=10, verbose_name='estado')
    fecha_inicio = models.DateField(null=False, verbose_name='fecha_inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='fecha_fin')
    cantidad_dias = models.IntegerField(verbose_name='cantidad_dias')
    forma_pago = models.CharField(max_length=10, verbose_name='forma_pago')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='modificado')
    huesped = models.ManyToManyField(Huesped, verbose_name='Huespedes', blank=False) 
    habitacion = models.ForeignKey(Habitacion, null=False, editable=False, verbose_name='habitacion', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, editable=False, verbose_name='usuario', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'
        db_table = 'estadias' 
        ordering = ['id_estadia']
        
    def __str__(self):
        return f"{self.id_estadia} - {self.estado}"