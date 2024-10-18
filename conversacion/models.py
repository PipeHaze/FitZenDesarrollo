from django.db import models
from django.conf import settings
from principal.models import Producto

# Create your models here.

class Conversacion(models.Model):
    producto = models.ForeignKey(Producto, related_name="conversaciones", on_delete=models.CASCADE)
    miembros = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversaciones")
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modificado_en',)
    
class ConversacionMensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, related_name="mensajes", on_delete=models.CASCADE)
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="mensajes_creados", on_delete=models.CASCADE)
