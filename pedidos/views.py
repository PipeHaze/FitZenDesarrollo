from django.shortcuts import render
from django.http.response import JsonResponse


from carritocompras.carritocompras import Carrito
from .models import Pedido, PedidoItem

# Create your views here.

def agregar(request):
    carrito = Carrito(request)#se crea la variable carrito para que acceda a la clase Carrito y a sus metodos
    if request.POST.get('action') == 'post':

        pedido_key = request.POST.get('order_key')#order_key es el nombre que se creo con el js para procesar el pago
        user_id = request.user.id
        
        carritototal = carrito.get_total_precio()# aqui carrito ocupa un metodo que es total_precio

        #comprobar si el pedido existe
        if Pedido.objects.filter(pedido_key = pedido_key).exists():
            pass
        else:
            pedido = Pedido.objects.create(user_id=user_id, nombre_completo = user_id, direccion1 = 'Volcan Guallatiri',
                                           direccion2 = 'Quilicura',total_pagado = carritototal, pedido_key=pedido_key)
            pedido_id = pedido.pk

            for item in carrito:
                PedidoItem.objects.create(pedido_id=pedido_id, producto=item['producto'],precio=item['precio'], cantidad=item['qty'])

    response = JsonResponse({'success': 'Devolver algo'})
    return response

def payment_confirmation(data):
    Pedido.objects.filter(pedido_key=data).update(estado_factura=True)
