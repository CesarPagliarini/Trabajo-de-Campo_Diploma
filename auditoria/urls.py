from django.urls import path
from . import views

urlpatterns = [
    path('auditoria_estadias/', views.InformeAuditoriaEstadias, name='auditoria_estadias'),
    path('auditoria_servicios/', views.InformeAuditoriaServicios, name='auditoria_servicios'),
    path('auditoria_accesos/', views.InformeAuditoriaAccesos, name='auditoria_accesos'),
]
