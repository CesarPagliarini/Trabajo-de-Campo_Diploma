from crum import get_current_user
from django.db import models
from django.contrib.auth.models import User
from auditoria.models import BaseAuditoria
from crum import get_current_user

# Create your models here.

class Huesped(BaseAuditoria):
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
    user = models.ForeignKey(User, null=True, blank=True, editable=False, verbose_name='Usuario', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Huesped'
        verbose_name_plural = 'Huespedes'
        db_table = 'huespedes' 
        
    def __str__(self):
        return f"{self.dni} - {self.nombre} {self.apellido}"
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user = user
        self.user_update = user
        super(Huesped, self).save(*args, **kwargs)