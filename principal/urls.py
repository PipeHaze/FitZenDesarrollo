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
        


]
