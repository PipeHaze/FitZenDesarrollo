from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Producto, Like
from .utils import decrypt_slug, encrypt_slug
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ProductoForm, ComentarioForm, EditarProducto
from django.contrib import messages
from django.db.models import Q
from cuentas.models import UserBase
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden







# Create your views here.

def paginaprincipal(request):
    producto = Producto.producto.filter(aprobado = True)  # Obtener todos los productos, al principio voy a traer todos los objetos, despues va a hacer con object or 404.
    return render(request,"app/paginaprincipal.html", {'producto': producto})

def pagina_info(request):
    return render(request, "app/pagina_info.html")

def producto_info(request, encrypted_slug):
    # Desencriptar el slug
    slug = decrypt_slug(encrypted_slug)

    producto = get_object_or_404(Producto, slug=slug, en_stock=True)
    return render(request, 'app/infoproductos.html', {'producto': producto})

def categoria_productos(request, categoria_slug = None):
    categoria = get_object_or_404(Categoria, slug = categoria_slug)
    productos = Producto.objects.filter(categoria = categoria)
    return render(request,'app/categorias.html', {'categoria': categoria, 'productos': productos})    

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
            return redirect(to='principal:agregarproducto')
    else:
        form = ProductoForm()
    return render(request, 'app/agregarproducto.html', {'form': form})

@permission_required('app.delete_producto')
def productos_pendientes(request):
    productos = Producto.objects.filter(aprobado = False) #es false porque primero se tiene que aprobar desde este html por el administrador
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

def ver_perfil(request, user_name=None):
    current_user = request.user

    if isinstance(current_user, AnonymousUser) or (user_name and user_name != current_user.user_name): # si el nombre de usuario es distinto al inicio de sesion actual, redirige al perfil de ese usuario
        user = get_object_or_404(UserBase, user_name=user_name)
    else:
        user = current_user

    return render(request, "account/user/dashboard.html", {'user': user})


def editarproducto(request, encrypted_slug):
    # Desencriptar el slug
    slug = decrypt_slug(encrypted_slug)
    
    # Obtener el producto usando el slug desencriptado
    producto = get_object_or_404(Producto, slug=slug, en_stock=True)
    
    # Verificar que el usuario tiene permiso para editar el producto
    if producto.creado_por != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permisos para editar este producto")
    
    if request.method == 'POST':
        form = EditarProducto(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            # Redirigir usando el slug encriptado nuevamente
            return redirect('principal:informacion_productos', encrypted_slug=producto.encrypted_slug)
    else:
        form = EditarProducto(instance=producto)
    
    return render(request, "app/editarproducto.html", {
        'form': form,
        'title': 'Editar tu producto'
    })

def eliminarproducto(request, slug):
    # Obtener el producto usando el slug
    producto = get_object_or_404(Producto, slug=slug, en_stock=True)
    
    # Verificar que el usuario tiene permiso para eliminar el producto
    if producto.creado_por != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permisos para eliminar este producto.")
    
    # Eliminar el producto
    producto.delete()
    
    return redirect('principal:paginaprincipal')
