from django.contrib import admin
from .models import Habitacion, TipoHabitacion, EstadoHabitacion

class EstadoHabitacionAdmin(admin.ModelAdmin):
    readonly_fields = ['nro_estado']
    search_fields = ('nro_estado', 'estado')                
    list_filter = ('nro_estado', 'estado')
    list_display = ('nro_estado', 'estado')
    ordering = ['nro_estado']
    
    
class HabitacionAdmin(admin.ModelAdmin):
    readonly_fields = ['nro_habitacion']
    search_fields = ('nro_habitacion', 'estado__estado')                
    list_filter = ('estado__estado', 'tipo_habitacion__nombre')                 # Filtro por nro_habitacion
    list_display = ('nro_habitacion', 'get_tipoHabitacion', 'get_estado')       # Agrega columnas
    
    def get_estado(self, obj):                                         # Obtiene la el valor del columna estado a traves de la ForeingKey
        return obj.estado.estado
    get_estado.short_description = 'estado'
    
    def get_tipoHabitacion(self, obj):                                # Obtiene la el valor del columna nombre a traves de la ForeingKey
        return obj.tipo_habitacion.nombre
    get_tipoHabitacion.short_description = 'tipoHabitacion'           # Cambia el nombre de la columna en el administrador
    
class TipoHabitacionAdmin(admin.ModelAdmin):
    readonly_fields = ['id_tipo_habitacion']
    search_fields = ('id_tipo_habitacion', 'nombre', 'capacidad', 'precio_por_noche')                
    list_filter = ('id_tipo_habitacion', 'nombre', 'capacidad')
    list_display = ('nombre', 'capacidad')
    ordering = ['id_tipo_habitacion']
    

# Register your models here.

admin.site.register(Habitacion, HabitacionAdmin)
admin.site.register(TipoHabitacion, TipoHabitacionAdmin)
admin.site.register(EstadoHabitacion, EstadoHabitacionAdmin)