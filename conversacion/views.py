from django.shortcuts import get_object_or_404, render, redirect
from principal.models import Producto
from .models import Conversacion, ConversacionMensaje
from .forms import ConversationMessageForm, ConversationMessageForm2
from django.contrib.auth.decorators import login_required


# Create your views here.
def nueva_conversacion(request, encrypted_slug):
    producto = get_object_or_404(Producto, slug = encrypted_slug, en_stock = True) #del modelo producto se traen las variables, la url encriptada y el stock si esta disponible

    if producto.creado_por == request.user:
        return redirect('principal:paginaprincipal')
    
    conversaciones = Conversacion.objects.filter(producto = producto).filter(miembros__in = [request.user.id])

    if conversaciones.exists():
        pass #si existe ignora este if pasa al otro

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            #crear conversaciones y miembros
            conversacion = Conversacion.objects.create(producto = producto)
            conversacion.miembros.add(request.user)
            conversacion.miembros.add(producto.creado_por)
            conversacion.save()

            #guardar los mensajes
            conversacion_mensaje = form.save(commit = False)
            conversacion_mensaje.conversacion = conversacion #cargar los objetos que tiene guardado conversacion
            conversacion_mensaje.creado_por = request.user
            conversacion_mensaje.save()

            return redirect('principal:informacion_productos', encrypted_slug = producto.encrypted_slug)
    else:
        form = ConversationMessageForm

    return render(request, 'conversacion/nuevaconversacion.html', {'form':form, 'producto':producto})

@login_required
def inbox(request):
    conversaciones = Conversacion.objects.filter(miembros__in=[request.user.id])

    return render(request, 'conversacion/inbox.html', {
        'conversaciones': conversaciones
    })

def detalle(request, pk):
    conversacion = Conversacion.objects.filter(miembros__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        form2 = ConversationMessageForm2(request.POST)

        if form.is_valid() or form2.is_valid():
            conversacion_mensaje = form.save(commit=False)
            conversacion_mensaje.conversacion = conversacion
            conversacion_mensaje.creado_por = request.user
            conversacion_mensaje.save()

            conversacion.save()
            

            return redirect('conversacion:detalle', pk=pk)
    else:
        form = ConversationMessageForm()
        form2 = ConversationMessageForm2()

    return render(request, 'conversacion/detalle.html', {
        'conversacion': conversacion,
        'form': form,
        'form2': form2,
    })