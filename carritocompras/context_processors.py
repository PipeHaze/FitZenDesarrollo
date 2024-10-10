from .carritocompras import Carrito

def carritocompras(request):
    return {'carritocompras': Carrito(request)}