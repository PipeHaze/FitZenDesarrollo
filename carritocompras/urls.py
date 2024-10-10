from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'carritocompras'

urlpatterns = [
    path('',views.carrito_resumen, name="carrito_resumen"),
    path('agregar/',views.carrito_agregar, name="carrito_agregar"),
    path('eliminar/',views.carrito_eliminar, name="carrito_eliminar"),
    path('modificar/',views.carrito_modificar, name="carrito_modificar"),

        
]