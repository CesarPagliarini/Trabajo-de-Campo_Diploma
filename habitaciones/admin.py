from django.contrib import admin
from .models import Habitacion, TipoHabitacion


class HabitacionAdmin(admin.ModelAdmin):
    readonly_fields = ['nro_habitacion']
    search_fields = ('nro_habitacion', 'estado')                
    list_filter = ('nro_habitacion', )                    # Filtro por nro_habitacion
    list_display = ('nro_habitacion', 'estado')           # Agrega columnas
        

class TipoHabitacionAdmin(admin.ModelAdmin):
    readonly_fields = ['id_tipo_habitacion']
    search_fields = ('id_tipo_habitacion', 'nombre', 'capacidad', 'precio_por_noche')                
    list_filter = ('id_tipo_habitacion', 'nombre', 'capacidad')
    list_filter = ('id_tipo_habitacion', 'nombre', 'capacidad', 'superficie')
    
# Register your models here.

admin.site.register(Habitacion, HabitacionAdmin)
admin.site.register(TipoHabitacion, TipoHabitacionAdmin)