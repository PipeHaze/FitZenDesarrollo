from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'foro'

urlpatterns = [
    path('foro_principal/', views.foro_principal, name='foro_principal'), #Listo
    path('foro_publicacion/<slug:encrypted_slug>/', views.foro_publicacion, name='foro_publicacion'), #Listo
    path('foro_publicacion/<int:post_id>/like/', views.like_post, name='like_post'), #Listo
    path('agregarforo/',views.agregarforo,name="agregarforo"), #Listo



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)