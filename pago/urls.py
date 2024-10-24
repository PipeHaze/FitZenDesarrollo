from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'pago'

urlpatterns = [
    path('', views.carritoViews, name='carritopago'),
    path('orderplaced/',views.order_placed, name= 'order_placed'),
    path('webhook/', views.stripe_webhook, name= 'stripe_webhook'),

]