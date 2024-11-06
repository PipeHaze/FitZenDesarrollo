from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Producto
from .utils import decrypt_slug
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ProductoForm
from django.contrib import messages
from django.db.models import Q



# Create your views here.

def paginaprincipal(request):
    producto = Producto.producto.filter(aprobado = True)  # Obtener todos los productos, al principio voy a traer todos los objetos, despues va a hacer con object or 404.
    return render(request,"app/paginaprincipal.html", {'producto': producto})

def producto_info(request, encrypted_slug):
    # Desencriptar el slug
    slug = decrypt_slug(encrypted_slug)

    producto = get_object_or_404(Producto, slug=slug, en_stock=True)
    return render(request, 'app/infoproductos.html', {'producto': producto})

def categoria_productos(request, categoria_slug = None):
    categoria = get_object_or_404(Categoria, slug = categoria_slug)
    productos = Producto.objects.filter(categoria = categoria)
    return render(request,'app/categorias.html', {'categoria': categoria, 'productos': productos})

def foro_principal(request):
    return render(request,'foro/foro_principal.html')

def foro_publicacion(request):
    return render(request,'foro/foro_publicacion.html')    

@login_required
def agregarproducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creado_por = request.user
            categoria_id = request.POST.get('categoria')
            # Asignar la categoría al producto
            producto.categoria_id = categoria_id
            producto.aprobado = False # QUE NO SE ME OLVIDE CAMBIARLO A FALSE PARA APROBAR EL PRODUCTO
            producto.save()
            messages.success(request, 'el producto se ha agregado, pero tiene que ser aprobado por el administrador')
            return redirect(to='principal:paginaprincipal')
    else:
        form = ProductoForm()
    return render(request, 'app/agregarproducto.html', {'form': form})

@permission_required('app.delete_producto')
def productos_pendientes(request):
    productos = Producto.objects.filter(aprobado = False)
    return render(request,'app/productos_pendientes.html', {'productos': productos})

@permission_required('app.add_producto')
def aprobar_producto(request, pk):
    producto = get_object_or_404(Producto, pk = pk)
    producto.aprobado = True
    producto.save()
    return redirect('principal:productos_pendientes')

@permission_required('app.delete_producto')
def rechazar_producto(request, pk):
    producto = get_object_or_404(Producto, pk = pk)
    producto.delete()
    return redirect('principal:productos_pendientes')

def buscar_pendientes(request):
    queryset = request.GET.get("buscar")#este es el nombre que sale el el buscador de la pagina productos pendientes.
    productos = Producto.objects.filter(aprobado=False)
    
    if queryset:
        productos = Producto.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(descripcion__icontains = queryset)
        ).distinct()
    
    return render(request, 'app/productos_pendientes.html', {'productos': productos})