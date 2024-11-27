from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'principal'

urlpatterns = [
        path('',views.paginaprincipal,name="paginaprincipal"), #Listo
        path('item/<str:encrypted_slug>/', views.producto_info, name='informacion_productos'), #Listo
        path('search/<slug:categoria_slug>/', views.categoria_productos, name='categoria_productos'), #Listo
        path('agregarproducto/',views.agregarproducto,name="agregarproducto"), #Listo
        path('productos_pendientes/',views.productos_pendientes,name="productos_pendientes"), #Listo
        path('aprobar_producto/<int:pk>/',views.aprobar_producto,name="aprobar_producto"), #Listo
        path('rechazar_producto/<int:pk>/',views.rechazar_producto,name="rechazar_producto"), #Listo
        path('buscar_pendientes/', views.buscar_pendientes, name='buscar_pendientes'), #Listo
        path('foro_principal/', views.foro_principal, name='foro_principal'), #Listo
        # urls.py
        path('foro_publicacion/<slug:encrypted_slug>/', views.foro_publicacion, name='foro_publicacion'), #Listo
        path('foro_publicacion/<int:post_id>/like/', views.like_post, name='like_post'), #Listo
        path('perfil/<str:user_name>/',views.ver_perfil, name='ver_perfil'), #listo
        path('pagina_info/', views.pagina_info, name='pagina_info'),
        path('editar_producto/<str:encrypted_slug>/', views.editarproducto, name='editar_producto'),
        path('eliminar_producto/<slug:slug>/',views.eliminarproducto, name='eliminar_producto'), 




]
