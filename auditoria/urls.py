from django.urls import path
from . import views

urlpatterns = [
    path('informe_auditoria', views.InformeAuditoriaEstadias, name='informe_auditoria'),
]
