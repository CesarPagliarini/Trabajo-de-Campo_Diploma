from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='index'),
    path('inicio/', views.index, name='inicio'),
    path('registro/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('alta_estadia/', views.formulario_estadia, name='alta_estadia'),
    path('listado_estadias/', views.listado_estadias, name='listado_estadias'),
    path('borrar_estadia/<int:id>', views.borrar_estadia, name="borrar_estadia"),
    path('editar_estadia/<int:id>', views.formulario_estadia, name="editar_estadia"),
    path('alta_estadia_inicio/', views.alta_estadia_inicio, name='alta_estadia_inicio'),
    path('alta_estadia_final/<int:cantidad_dias>/<int:habitacion>', views.alta_estadia_final, name='alta_estadia_final'),
]
