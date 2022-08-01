from django.contrib import admin
from servicios.models import EstadoReserva, Servicio, ReservaServicio

# Register your models here.

class ServicioAdmin(admin.ModelAdmin):
    readonly_fields = ['id_servicio', ]
    search_fields = ('id_servicio', 'servicio', 'precio') 
    list_filter = ('servicio', )         
    list_display = ('id_servicio', 'servicio', 'precio')         # Agrega columnas
    

class EstadoReservaAdmin(admin.ModelAdmin):
    readonly_fields = ['nro_estado']
    search_fields = ('nro_estado', 'estado') 
    list_filter = ('estado', )         
    list_display = ('nro_estado', 'estado')    
    
     
class ReservaServicioAdmin(admin.ModelAdmin):
    readonly_fields = ['id_reserva', 'created_at', 'updated_at', 'user']
    search_fields = ('ir_reserva', 'get_estado')       
    list_display = ('id_reserva', 'get_estado')
    
    def get_estado(self, obj):                                         # Obtiene la el valor del columna estado a traves de la ForeingKey
        return obj.estado.estado
    get_estado.short_description = 'estado'
    
    def save_model(self, request, obj, form, change):
       if not obj.user_id:
           obj.user_id = request.user.id                   # Si no trae el id de usuario, le asigna el del usuario actual (Logueado)
       obj.save()                                          # Guarda el objeto del usuario
        
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(EstadoReserva, EstadoReservaAdmin)
admin.site.register(ReservaServicio, ReservaServicioAdmin)
