from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class ReporteEstadias(TemplateView):
    template_name = 'reportes/reporte.html'
