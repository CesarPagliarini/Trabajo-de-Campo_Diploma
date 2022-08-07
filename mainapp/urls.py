from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='index'),
    path('inicio/', views.index, name='inicio'),
    path('registro/', views.register_page, name='register'),
    path('modificar_usuario/<int:id>', views.register_page, name='modificar_usuario'),
    path('listado_usuarios/', views.listado_usuarios, name='listado_usuarios'),
    path('alta_grupo/', views.alta_grupo, name='alta_grupo'),
    path('modificar_grupo/<int:id>', views.alta_grupo, name='modificar_grupo'),
    path('listado_grupos/', views.listado_grupos, name='listado_grupos'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('alta_estadia_inicio/', views.alta_estadia_inicio,name='alta_estadia_inicio'),
    path('alta_estadia_final/<int:dia_inicio>/<int:mes_inicio>/<int:anio_inicio>/<int:dia_fin>/<int:mes_fin>/<int:anio_fin>/<int:cantidad_dias>/<int:habitacion>',views.alta_estadia_final, name='alta_estadia_final'),
    path('listado_estadias/', views.listado_estadias, name='listado_estadias'),
    path('borrar_estadia/<int:id>', views.borrar_estadia, name="borrar_estadia"),
    path('editar_estadia/<int:id>/<int:estado>', views.editar_estadia, name="editar_estadia"),
    path('editar_estadia_final/<int:id>/<int:habitacion>', views.editar_estadia_final, name="editar_estadia_final"),
    path('checkin-out_estadia/<int:id>/<str:accion>/<int:estado>', views.checkin_checkout_estadia, name="checkin-out_estadia"),
]
