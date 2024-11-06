from django.db import models
from decimal import Decimal
from django.conf import settings

from principal.models import Producto


#crear modelos

class Pedido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedido_user')
    nombre_completo = models.CharField(max_length=50)
    direccion1 = models.CharField(max_length=250)
    direccion2 = models.CharField(max_length=250, blank=True, null=True)  # Cambié a opcional
    ciudad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, blank=True, null=True)  # Nuevo campo
    pais = models.CharField(max_length=100, blank=True, null=True)  # Nuevo campo
    region = models.CharField(max_length=100, blank=True, null=True)  # Nuevo campo
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    total_pagado = models.DecimalField(max_digits=7, decimal_places=3)
    pedido_key = models.CharField(max_length=200)
    estado_factura = models.BooleanField(default=True)

    class Meta:
        ordering = ('-creado',)

    def __str__(self):
        return str(self.creado)
    
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido,
                              related_name='items',
                              on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,
                                 related_name='pedido_items',
                                 on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=7, decimal_places=3)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
