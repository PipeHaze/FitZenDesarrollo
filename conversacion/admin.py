from django.contrib import admin
from .models import Conversacion, ConversacionMensaje

# Register your models here.
admin.site.register(ConversacionMensaje)
admin.site.register(Conversacion)
