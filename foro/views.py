from .models import Foro
from principal.utils import decrypt_slug, encrypt_slug
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ComentarioForm, ForoForm, EditarForo
from principal.models import Like
from django.contrib import messages
from django.http import HttpResponseForbidden





# Create your views here.

def foro_principal(request):
    # Obtén todos los foros
    foros = Foro.objects.all()
    foros_con_comentarios = []

    for foro in foros:
        comentarios = foro.comentarios.filter(activo=True)  # Filtra comentarios activos relacionados con el foro
        foro.conteo_comentarios = comentarios.count()  # Agrega el conteo de comentarios al objeto foro
        foros_con_comentarios.append(foro)

    # Renderiza la plantilla
    return render(request, 'foro/foro_principal.html', {"foro_productos": foros_con_comentarios})


def foro_publicacion(request, encrypted_slug):
    slug = decrypt_slug(encrypted_slug)
    foro = get_object_or_404(Foro, slug=slug)
    comentarios = foro.comentarios.filter(activo=True, comentario_padre=None)
    usuarios_que_dieron_like = foro.likes.values_list('user_id', flat=True)

    form = ComentarioForm()

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_form = form.save(commit=False)
            nuevo_form.usuario = request.user
            nuevo_form.producto_foro = foro

            # Identificar si es respuesta a un comentario
            comentario_padre_id = request.POST.get("comentario_padre_id")
            if comentario_padre_id:
                nuevo_form.comentario_padre_id = comentario_padre_id
            
            nuevo_form.save()
            return redirect('foro:foro_publicacion', encrypted_slug=foro.encrypted_slug)

    return render(request, 'foro/foro_publicacion.html', {
        'foro': foro,
        'comentarios': comentarios,
        'form': form,
        'usuarios_que_dieron_like': usuarios_que_dieron_like,
    })

def like_post(request, post_id):
    foro = get_object_or_404(Foro, id=post_id) #se le pasa el atributo foro del model
    like, created = Like.objects.get_or_create(foro=foro, user=request.user) #el modelo like contiene la llave foranea de foro, la usamos aqui
    
    if not created:
        # Si el like ya existe, se elimina
        like.delete()
        
    # Cifrar el slug antes de redirigir
    encrypted_slug = encrypt_slug(foro.slug)
    return redirect('foro:foro_publicacion', encrypted_slug=encrypted_slug)

def agregarforo(request):
    if request.method == 'POST':
        form = ForoForm(request.POST, request.FILES)
        if form.is_valid():
            foro = form.save(commit=False)
            foro.creado_por = request.user
            # Asignar la categoría al producto
            foro.save()
            messages.success(request, 'Se ha agregado el foro, muchas gracias por tu visita.')
            return redirect(to='foro:foro_principal')
    else:
        form = ForoForm()
    return render(request, 'Foro/agregarforo.html', {'form': form})

def eliminarforo(request, slug):
    # Obtener el producto usando el slug
    foro = get_object_or_404(Foro, slug=slug)
    
    # Verificar que el usuario tiene permiso para eliminar el producto
    if foro.creado_por != request.user and not request.user.is_superuser: #el foro despues del . son las propiedades que contiene el modelo del foro
        return HttpResponseForbidden("No tienes permisos para eliminar este producto.")
    
    # Eliminar el producto
    foro.delete()
    
    return redirect('foro:foro_principal')

def editarforo(request, encrypted_slug):
    # Desencriptar el slug
    slug = decrypt_slug(encrypted_slug)
    
    # Obtener el producto usando el slug desencriptado
    foro = get_object_or_404(Foro, slug=slug)
    
    # Verificar que el usuario tiene permiso para editar/eliminar el producto
    if foro.creado_por != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permisos para editar o eliminar este producto.")
    
    if request.method == 'POST':
        form = EditarForo(request.POST, request.FILES, instance=foro)
        if form.is_valid():
            form.save()
            # Redirigir usando el slug encriptado nuevamente
            return redirect('foro:foro_principal')
    else:
        form = EditarForo(instance=foro)
    
    return render(request, "foro/editarforo.html", {
        'form': form,
        'title': 'Editar foro publicado'
    })
