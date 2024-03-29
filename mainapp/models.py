from unicodedata import decimal
from django.db import models
from django.contrib.auth.models import User
from huespedes.models import Huesped
from habitaciones.models import Habitacion
from auditoria.models import BaseAuditoria
from crum import get_current_user

# Create your models here.

# Aplicacion Singletone
#class Reglamento(models.Model):
#    retiro_anticipado = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='tasa')
    
#    def __str__(self):
#        return "reglamento"
    
#    @classmethod
#    def get_instancia(cls):
#        instancia, creado = Reglamento.objects.get_or_create(pk=1, defaults={
#            'retiro_anticipado': 0.99
#            })
#        return instancia
 
class Reglamento(object):
    instance = None
    
    def __new__(cls):
        if cls.instance is not None:
            return cls.instance
        else:
            inst = cls.instance = super(Reglamento, cls).__new__()
            return inst
          
#Reglamento.get_instancia().retiro_anticipado       # Uso de la instanciacion
      
class EstadoEstadia(models.Model):
    nro_estado = models.AutoField(primary_key=True, editable=False, verbose_name='nro_estado')
    estado = models.CharField(max_length=10, verbose_name='estado')
    
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        db_table = 'estados_estadia'
        ordering = ['nro_estado']
        
    def __str__(self):
        return f"{self.nro_estado} - {self.estado}"
  
    
class FormasPago(models.Model):
    id_formaPago = models.AutoField(primary_key=True, editable=False, verbose_name='id_formaPago')
    descripcion = models.CharField(max_length=15, verbose_name='descripcion')
    
    class Meta:
        verbose_name = 'FormaPago'
        verbose_name_plural = 'FormasPago'
        db_table = 'forma_pago'
        ordering = ['id_formaPago']
        
    def __str__(self):
        return f"{self.id_formaPago} - {self.descripcion}"
    
        
class Estadia(BaseAuditoria):
    id_estadia = models.AutoField(primary_key=True, editable=False, verbose_name='id_estadia')
    fecha_inicio = models.DateField(null=False, verbose_name='fecha_inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='fecha_fin')
    cantidad_dias = models.IntegerField(verbose_name='cantidad_dias')
    huesped = models.ManyToManyField(Huesped, verbose_name='Huespedes', blank=False) 
    #forma_pago = models.ForeignKey(FormasPago, null=True, blank=True, editable=True, verbose_name='forma_pago', on_delete=models.CASCADE)
    penalizacion = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=2, verbose_name='penalizacion')
    estado = models.ForeignKey(EstadoEstadia, null=False, editable=True, verbose_name='estado', on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, null=False, editable=True, verbose_name='habitacion', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'
        db_table = 'estadias' 
        ordering = ['id_estadia']
        
    def __str__(self):
        return f"{self.id_estadia} - {self.estado.estado} - {self.habitacion.nro_habitacion}"
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user = user
        self.user_update = user
        super(Estadia, self).save(*args, **kwargs)
    
    
class EstadosDecuentos(models.Model):
    nro_estado = models.AutoField(primary_key=True, editable=False, verbose_name='nro_estado')
    estado = models.CharField(max_length=10, verbose_name='estado')
    
    class Meta:
        verbose_name = 'Estado Descuento'
        verbose_name_plural = 'Estados Decuentos'
        db_table = 'estados_descuento'
        ordering = ['estado']
        
    def __str__(self):
        return f"{self.nro_estado} - {self.estado}"
    
# Posible aplicacion de Singleton
class Descuentos(models.Model):
    id_descuento = models.AutoField(primary_key=True, unique=True, null=False, editable=False, verbose_name='id_descuento')
    descripcion = models.CharField(max_length=12, null=False, verbose_name='descripcion')                          # Ejemplo: 25%
    multiplicador = models.DecimalField(max_digits=4, decimal_places=3, null=False, verbose_name='multiplicador')   # Ejemplo: 0.125
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name='fecha_creacion')
    fecha_utilizacion = models.DateField(null=True, blank=True, editable=False, verbose_name='fecha_utilizacion')
    estado = models.ForeignKey(EstadosDecuentos, null = False, verbose_name='estado', on_delete=models.CASCADE)
    estadia = models.ForeignKey(Estadia, null=True, blank=True, editable=True, verbose_name='estadia', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
        db_table = 'descuentos' 
        ordering = ['id_descuento']
        
    def __str__(self):
        return f"{self.id_descuento} - {self.descripcion}"