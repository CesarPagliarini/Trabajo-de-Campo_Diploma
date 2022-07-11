from django.contrib import admin
from gzip import READ
from .models import Huesped

# Configuracion extra


class HuespedesAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'created_at', 'updated_at')
    search_fields = ('dni', 'apellido')                        # Buscador por dni y apellido
    list_filter = ('dni', )                                 # Filtro por dni
    list_display = ('dni', 'nombre', 'apellido')           # Agrega columnas
    
    def save_model(self, request, obj, form, change):
	    if not obj.user_id:
		    obj.user_id = request.user.id							# Si no trae el id de usuario, le asigna el del usuario actual (Logueado)
        
    
# Register your models here.

admin.site.register(Huesped, HuespedesAdmin)

# Configuracion del menu
title = "Sistema de Gestión hotelera"
subtitle = "Panel de gestion"


admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle