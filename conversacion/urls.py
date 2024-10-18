from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'conversacion'

urlpatterns = [
    path('nuevo/<slug:encrypted_slug>/', views.nueva_conversacion, name='nuevaconversacion'),
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detalle, name='detalle'),



]