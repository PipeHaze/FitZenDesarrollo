from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Producto
from .utils import decrypt_slug


# Create your views here.

def paginaprincipal(request):
    producto = Producto.objects.all()  # Obtener todos los productos, al principio voy a traer todos los objetos, despues va a hacer con object or 404.
    return render(request,"app/paginaprincipal.html", {'producto': producto})

def producto_info(request, encrypted_slug):
    # Desencriptar el slug
    slug = decrypt_slug(encrypted_slug)

    producto = get_object_or_404(Producto, slug=slug, en_stock=True)
    return render(request, 'app/infoproductos.html', {'producto': producto})
