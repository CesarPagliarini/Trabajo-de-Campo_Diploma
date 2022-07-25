from django.contrib import admin
from .models import Estadia, Descuentos, EstadoEstadia, FormasPago, EstadosDecuentos


# Configuracion del menu
title = "Sistema de Gestión hotelera"
subtitle = "Panel de gestion"


class EstadiaAdmin(admin.ModelAdmin):
    readonly_fields = ['id_estadia', 'user', 'created_at', 'updated_at']
    search_fields = ('get_estado', 'fecha_inicio', 'fecha_fin')                
    list_filter = ('habitacion__nro_habitacion', )                                 # Filtro por nro_habitacion
    list_display = ('id_estadia', 'get_habitacion', 'get_estado', 'fecha_inicio', 'fecha_fin', 'cantidad_dias')       # Agrega columnas
    
    def get_estado(self, obj):                                         # Obtiene la el valor del columna estado a traves de la ForeingKey
        return obj.estado.estado
    get_estado.short_description = 'estado'
    
    def get_habitacion(self, obj):                                     # Obtiene la el valor del columna nro_habitacion a traves de la ForeingKey
        return obj.habitacion.nro_habitacion
    get_habitacion.short_description = 'habitacion'
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user_id = request.user.id                               # Si no trae el id de usuario, le asigna el del usuario actual (Logueado)
        obj.save()                                                      # Guarda el objeto del usuario
       
class DescuentoAdmin(admin.ModelAdmin):
    readonly_fields = ['id_descuento']
    search_fields = ('id_descuento', 'estado', 'multiplicador') 
    list_filter = ('multiplicador', )         
    list_display = ('id_descuento', 'multiplicador', 'estado')         # Agrega columnas

class EstadosDescuentosAdmin(admin.ModelAdmin):
    readonly_fields = ['nro_estado']
    search_fields = ['estado'] 
    list_filter = ['estado']          
    list_display = ('nro_estado', 'estado')                           # Agrega columnas
    
class EstadosAdmin(admin.ModelAdmin):
    readonly_fields = ['nro_estado']
    search_fields = ['estado'] 
    list_filter = ['estado']          
    list_display = ('nro_estado', 'estado')                           # Agrega columnas
    
class FormasPagoAdmin(admin.ModelAdmin):
    readonly_fields = ['id_formaPago']
    search_fields = ['descripcion'] 
    list_filter = ['descripcion']         
    list_display = ('id_formaPago', 'descripcion')                  # Agrega columnas
    
# Register your models here.

admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle

admin.site.register(Estadia, EstadiaAdmin)
admin.site.register(Descuentos, DescuentoAdmin)
admin.site.register(EstadosDecuentos, EstadosDescuentosAdmin)
admin.site.register(EstadoEstadia, EstadosAdmin)
admin.site.register(FormasPago, FormasPagoAdmin)