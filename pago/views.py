from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from carritocompras.carritocompras import Carrito
from pedidos.views import payment_confirmation


import stripe
import json

# Create your views here.

@login_required
def carritoViews(request):

    carrito = Carrito(request)
    total = str(carrito.get_total_precio())
    total = total.replace('.','') #separacion de miles
    total = int(total) #mostrar el total de la compra en general

    print('total')

    stripe.api_key = 'sk_test_51MZdL1AwsCqvVI3W02kUNOcr4HdcVKvHxef2HOwp8nwaLXhT80orXE3GTdnNxRgS3Gqmjxig7xbrlSflWqxciCyc00CTMBsHHN' #la key de stripe para procesar el pago
    intent = stripe.PaymentIntent.create( #estas son las variables que vienen definidas por stripe, que se encuentran en la pagina
        amount= total,
        currency='clp', #formato de moneda chilena
        metadata={'userid': request.user.id}
    )

    return render(request,'pago/registropago.html', {'client_secret': intent.client_secret})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    

    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    
    else:
        print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)
    
def order_placed(request):
    carrito = Carrito(request)

    for i in carrito:
        carrito.disminuirStock(i["id_producto"]) #esta funcion es llamada para que al procesar el pago descuente los productos

    carrito.clear()
    return render(request, 'pago/pedidorealizado.html')
