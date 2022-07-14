from django.urls import path
from huespedes.views import formularioHuesped, listado_huespedes, borrar_huesped, editar_huesped

urlpatterns = [
  path('alta_huesped/', formularioHuesped, name="alta_huesped"),
  path('listado_huespedes/', listado_huespedes, name="listado_huespedes"),
  path('borrar_huesped/<int:id>', borrar_huesped, name="borrar_huesped"),
  path('editar_huesped/<int:id>', editar_huesped, name="editar_huesped"),
]