from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseAuditoria(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    user = models.ForeignKey(User, null=True, blank=True, editable=False, verbose_name='Usuario', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_creation')
    user_update = models.ForeignKey(User, null=True, blank=True, editable=False, verbose_name='Usuario_updated', on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_updated')
    
    class Meta:
        abstract = True
        
        
class ActividadUsuario(models.Model):
    usuario = models.ForeignKey('auth.User', verbose_name='Usuario', on_delete=models.CASCADE)
    login = models.DateTimeField(null = True, verbose_name='Login')
    logout = models.DateTimeField(null = True, verbose_name='Logout')
    creado = models.DateTimeField(auto_now_add = True, editable= False, verbose_name='Creado')   # Para diferenciar cronologicamente todos los registros
    
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        db_table = 'actividades'
        ordering = ['creado']

    def __str__(self):
        return self.usuario