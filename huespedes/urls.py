from django.urls import path
from huespedes.views import formularioHuesped

urlpatterns = [
  path('alta_huesped/', formularioHuesped, name="alta_huesped"),
]