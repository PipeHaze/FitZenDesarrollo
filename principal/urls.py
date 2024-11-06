from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'principal'

urlpatterns = [
        path('',views.paginaprincipal,name="paginaprincipal"),
        path('item/<str:encrypted_slug>/', views.producto_info, name='informacion_productos'),
        path('search/<slug:categoria_slug>/', views.categoria_productos, name='categoria_productos'),
        path('agregarproducto/',views.agregarproducto,name="agregarproducto"),
        path('productos_pendientes/',views.productos_pendientes,name="productos_pendientes"),
        path('aprobar_producto/<int:pk>/',views.aprobar_producto,name="aprobar_producto"),
        path('rechazar_producto/<int:pk>/',views.rechazar_producto,name="rechazar_producto"),
        path('buscar_pendientes/', views.buscar_pendientes, name='buscar_pendientes'),
        path('foro_principal/', views.foro_principal, name='foro_principal'),
        path('foro_publicacion/', views.foro_publicacion, name='foro_publicacion')

        


]
