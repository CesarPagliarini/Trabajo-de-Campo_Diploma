from django.urls import path
from . import views

urlpatterns = [
  path('reporte_estadias', views.ReporteEstadias, name='reporte_estadias'),
]
