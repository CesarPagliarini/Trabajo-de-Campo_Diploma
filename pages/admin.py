from django.contrib import admin
from .models import Page

# Configuracion extra

class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'content')                        # Buscador por titulo
    list_filter = ('visible', )                                 # Filtro si esta visible o no
    list_display = ('title', 'visible', 'created_at')           # Agrega columnas

# Register your models here.

admin.site.register(Page, PageAdmin)

# Configuracion del menu
title = "Proyecto con Django"
subtitle = "Panel de gestion"


admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle