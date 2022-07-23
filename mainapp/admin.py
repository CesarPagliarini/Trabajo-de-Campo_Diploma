from django.contrib import admin
from .models import Estadia, Descuentos


# Configuracion del menu
title = "Sistema de Gestión hotelera"
subtitle = "Panel de gestion"


class EstadiaAdmin(admin.ModelAdmin):
    readonly_fields = ['id_estadia', 'user', 'created_at', 'updated_at']
    search_fields = ('estado', 'fecha_inicio', 'fecha_fin')                
    list_filter = ('habitacion__nro_habitacion', )                                 # Filtro por nro_habitacion
    list_display = ('id_estadia', 'estado', 'fecha_inicio', 'fecha_fin')           # Agrega columnas
    
    
class DescuentoAdmin(admin.ModelAdmin):
    readonly_fields = ['id_descuento']
    search_fields = ('id_descuento', 'estado', 'multiplicador') 
    list_filter = ('multiplicador', )         
    list_display = ('id_descuento', 'multiplicador', 'estado')           # Agrega columnas

# Register your models here.

admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle

admin.site.register(Estadia, EstadiaAdmin)
admin.site.register(Descuentos, DescuentoAdmin)