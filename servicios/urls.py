from django.urls import path
from . import views

urlpatterns = [
    path('listado_reservas_servicios/', views.listado_reservas_servicios, name='listado_reservas_servicios'),
    path('borrar_reserva_servicio/<int:id>', views.borrar_reserva_servicio, name="borrar_reserva_servicio"),
    path('alta_reserva_servicio_inicio/', views.alta_reserva_inicio, name='alta_reserva_servicio_inicio'),
    path('alta_reserva_servicio_final/<int:id_estadia>/<int:dia>/<int:mes>/<int:anio>/<int:id_servicio>', views.alta_reserva_servicio_final, name='alta_reserva_servicio_final'),
    path('editar_reserva_servicio_inicio/<int:id>/<int:estado>', views.editar_reserva_servicio, name="editar_reserva_servicio_inicio"),
    path('editar_reserva_servicio_final/<int:id>/<int:servicio>', views.editar_reserva_servicio_final, name="editar_reserva_servicio_final"),
    path('tomar_reserva_servicio/<int:id>/<int:estado>', views.tomar_reserva_servicio, name="tomar_reserva_servicio"),
]