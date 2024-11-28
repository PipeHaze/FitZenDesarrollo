from django.contrib import admin
from .models import Foro

@admin.register(Foro)
class ForoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'descripcion']
