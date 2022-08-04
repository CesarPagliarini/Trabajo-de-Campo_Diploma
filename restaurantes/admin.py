from django.contrib import admin
from restaurantes.models import EstadoReservaRestaurante, Restaurante, ReservaRestaurante, TipoRestaurante, TurnoReserva

# Register your models here.

class TipoRestauranteAdmin(admin.ModelAdmin):
    readonly_fields = ['id_tipo_restaurante', ]
    search_fields = ('id_tipo_restaurante', 'descripcion') 
    list_filter = ('descripcion', )         
    list_display = ('id_tipo_restaurante', 'descripcion')         # Agrega columnas
    
    
class RestauranteAdmin(admin.ModelAdmin):
    readonly_fields = ['id_restaurante', ]
    search_fields = ('id_restaurante', 'nombre') 
    list_filter = ('nombre', )         
    list_display = ('id_restaurante', 'nombre', 'get_descripcion')         # Agrega columnas

    def get_descripcion(self, obj):                                         # Obtiene la el valor del columna estado a traves de la ForeingKey
        return obj.tipo_restaurante.descripcion
    get_descripcion.short_description = 'descripcion'
    
    
class EstadoReservaRestauranteAdmin(admin.ModelAdmin):
    readonly_fields = ['id_estado', ]
    search_fields = ('id_estado', 'estado') 
    list_filter = ('estado', )         
    list_display = ('id_estado', 'estado')         # Agrega columnas


class TurnoReservaAdmin(admin.ModelAdmin):
    readonly_fields = ['id_turno', ]
    search_fields = ('id_turno', 'horario') 
    list_filter = ('horario', )         
    list_display = ('id_turno', 'horario')         # Agrega columnas
    
    
class ReservaRestauranteAdmin(admin.ModelAdmin):
    readonly_fields = ['id_reserva', ]
    search_fields = ('id_reserva', 'restaurante', 'estado') 
    list_filter = ('restaurante', )         
    list_display = ('id_reserva', 'restaurante', 'get_restaurante', 'get_estado')         # Agrega columnas

    def get_restaurante(self, obj):                                         # Obtiene la el valor del columna estado a traves de la ForeingKey
        return obj.restaurante.nombre
    get_restaurante.short_description = 'restaurante'
    
    def get_estado(self, obj):                                         # Obtiene la el valor del columna estado a traves de la ForeingKey
        return obj.estado.estado
    get_estado.short_description = 'estado'
    
 
admin.site.register(Restaurante, RestauranteAdmin)
admin.site.register(EstadoReservaRestaurante, EstadoReservaRestauranteAdmin)
admin.site.register(ReservaRestaurante, ReservaRestauranteAdmin)
admin.site.register(TipoRestaurante, TipoRestauranteAdmin)
admin.site.register(TurnoReserva, TurnoReservaAdmin)