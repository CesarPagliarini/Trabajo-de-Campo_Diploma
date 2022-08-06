from django.urls import path
from . import views

urlpatterns = [
    path('listado_reservas_restaurantes/', views.listado_reservas_restaurantes, name='listado_reservas_restaurantes'),
    path('detalles_restaurante/<int:id>', views.detalles_restaurante, name='detalles_restaurante'),
    path('borrar_reserva_restaurante/<int:id>', views.borrar_reserva_restaurante, name="borrar_reserva_restaurante"),
    path('alta_reserva_restaurante_inicio/', views.alta_reserva_restaurante_inicio, name='alta_reserva_restaurante_inicio'),
    path('alta_reserva_restaurante_final/<int:id_estadia>/<int:dia>/<int:mes>/<int:anio>/<int:id_restaurante>/<int:horario>', views.alta_reserva_restaurante_final, name='alta_reserva_restaurante_final'),
    path('editar_reserva_restaurante_inicio/<int:id>/<int:estado>', views.editar_reserva_restaurante, name="editar_reserva_restaurante_inicio"),
    path('editar_reserva_restaurante_final/<int:id>/<int:restaurante>', views.editar_reserva_restaurante_final, name="editar_reserva_restaurante_final"),
     path('tomar_reserva_restaurante/<int:id>/<int:estado>', views.tomar_reserva_restaurante, name="tomar_reserva_restaurante"),
]