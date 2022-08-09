from django.urls import path
from . import views

urlpatterns = [
  path('reporte_servicios', views.ReporteServicios, name='reporte_servicios'),
  path('reporte_restaurantes', views.ReporteRestaurantes, name='reporte_restaurantes'),
]
