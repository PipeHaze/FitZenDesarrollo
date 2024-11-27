from django.shortcuts import render
from .carritocompras import Carrito
from django.shortcuts import get_object_or_404
from principal.models import Producto
from django.http import JsonResponse
from decimal import Decimal



# Create your views here.

app_name = 'carritocompras'

def carrito_resumen(request):
    carritocompras = Carrito(request)
    return render(request, 'carrito/resumencarrito.html',{'carritocompras': carritocompras})

def carrito_agregar(request):
    """
    Agrega un producto al carro de compras mediante el id, producto y la cantidad de los productos
    """
    carritocompras = Carrito(request)
    if request.POST.get('action') == 'post':
        producto_id = int(request.POST.get('productoid'))
        producto_qty = int(request.POST.get('productoqty'))
        producto = get_object_or_404(Producto, id=producto_id)
        carritoqty = carritocompras.__len__()
        carritocompras.agregar(producto = producto, qty = producto_qty)
        response = JsonResponse({'qty': carritoqty})
        return response
    
def carrito_eliminar(request):
    carritocompras = Carrito(request)
    if request.POST.get('action') == 'post':
        producto_id = int(request.POST.get('productoid'))
        carritocompras.eliminar(producto=producto_id)

        carritoqty = carritocompras.__len__()
        carritosubtotal = carritocompras.get_subtotal_precio() if carritoqty > 0 else Decimal(0)
        carritototal = carritocompras.get_total_precio() if carritoqty > 0 else Decimal(0)

        response = JsonResponse({
            'qty': carritoqty,
            'subtotal': float(carritosubtotal),  # Convertimos a float para JSON
            'total': float(carritototal)
        })
        return response


def carrito_modificar(request):
    carritocompras = Carrito(request)
    if request.POST.get('action') == 'post':
        producto_id = int(request.POST.get('productoid'))
        producto_qty = int(request.POST.get('productoqty'))
        carritocompras.modificar(producto = producto_id, qty = producto_qty)

        carritoqty = carritocompras.__len__()
        carritosubtotal = carritocompras.get_subtotal_precio()
        response = JsonResponse({'qty': carritoqty, 'subtotal': carritosubtotal})
        
        return response
    




