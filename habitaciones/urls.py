from django.urls import path
from . import views

urlpatterns = [
    path('listado_habitaciones/', views.listado_habitaciones,name='listado_habitaciones'),
]