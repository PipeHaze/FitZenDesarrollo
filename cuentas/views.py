from django.shortcuts import render, redirect
from .forms import RegistrationForm,UserEditForm, UserAddressForm, PerfilEditForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserBase, Direccion
from django.contrib.auth import login, logout
from .token import account_activation_token
from django.contrib.auth.decorators import login_required, permission_required
from pedidos.views import pedido_usuarios
from django.urls import reverse
from django.shortcuts import get_object_or_404
from principal.models import Producto
from django.contrib import messages





# Create your views here.

from django.core.mail import send_mail

def registro_usuarios(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Configurar email
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Enviar correo
            send_mail(
                subject,
                message,
                'felipe.morgado2000@gmail.com',  # Remitente
                [user.email],  # Destinatario
                fail_silently=False,
            )
            return HttpResponse('Registro exitoso, se ha enviado la activación.')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/registro.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserBase.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, '¡Tu cuenta ha sido activada con éxito!')
        return redirect('principal:paginaprincipal')
    else:
        messages.error(request, 'El enlace de activación no es válido o ha expirado.')
        return render(request, 'account/registration/activation_invalid.html')
    
@login_required
def dashboard(request): #trae los pedidos de los usuarios de esta vista creada
    return render(request,'account/user/dashboard.html')

def acciones_usuario(request):
    return render(request,'account/user/acciones_usuario.html')

def editar_detalles(request):
    """
    funcion que permite modificar el nombre de usuario en el dashboard
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST) #formulario para editar usuario
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,'account/user/editar_detalles.html', {'user_form': user_form})

@login_required
def borrar_usuarios(request): #se llama a esta funcion para que elimine la cuenta en el html.
    """
    funcion que desactiva una cuenta, ya que en la base de datos el usuario no se borra
    """
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request) #cuando se "borra el usuario, se cierra la sesion, el usuario no puede volver a logearse"
    return redirect('cuentas:confirma_eliminacion')

@login_required
def ver_pedidos_usuarios(request):
    pedido = pedido_usuarios(request) #trae los pedidos de los usuarios de esta vista creada
    return render(request,
                  'account/user/lista_pedidos_usuario.html', {'pedido': pedido})

@login_required
def ver_direccion(request):
    direcciones = Direccion.objects.filter(usuario=request.user) #filtrar las direcciones por el usuario logeado
    return render(request, "account/user/direcciones.html", {"direcciones": direcciones})

@login_required
def agregar_direccion(request):
    if request.method == "POST":
        direccion_form = UserAddressForm(data=request.POST)
        if direccion_form.is_valid():
            direccion_form = direccion_form.save(commit=False)
            direccion_form.usuario = request.user
            direccion_form.save()
            return HttpResponseRedirect(reverse("cuentas:direcciones"))
    else:
        direccion_form = UserAddressForm()
    return render(request, "account/user/editar_direccion.html", {"form": direccion_form})

@login_required
def editar_direccion(request, id):
    if request.method == "POST":
        direccion = Direccion.objects.get(pk=id, usuario = request.user)
        direccion_form = UserAddressForm(instance=direccion, data=request.POST)
        if direccion_form.is_valid():
            direccion_form.save()
            return HttpResponseRedirect(reverse("cuentas:direcciones"))
        
    else:
        direccion = Direccion.objects.get(pk=id, usuario = request.user)
        direccion_form = UserAddressForm(instance=direccion)
    return render(request, "account/user/editar_direccion.html", {"form": direccion_form})

@login_required
def eliminar_direccion(request, id):
    direccion = Direccion.objects.get(pk=id, usuario=request.user).delete() #filtra la direccion del usuario y delete la elimina.
    return redirect("cuentas:direcciones")

@login_required
def set_default(request, id):
    Direccion.objects.filter(usuario=request.user, default = True).update(default = False)
    Direccion.objects.filter(pk=id, usuario=request.user).update(default=True)
    return redirect("cuentas:direcciones")

@login_required
def editar_perfil(request, user_id):
    user = UserBase.objects.get(pk=user_id)
    
    # Verifica si el usuario autenticado es el propietario del perfil
    if request.user != user:
        # Redirige a una página de error o muestra un mensaje de error
        return redirect('cuentas:dashboard')

    if request.method == 'POST':
        form_user = PerfilEditForm(request.POST, request.FILES, instance=user.perfil)
        if form_user.is_valid():
            form_user.save()
            return redirect('cuentas:dashboard')
    else:
        form_user = PerfilEditForm(instance=user.perfil)
    
    return render(request, 'account/user/editar_perfil.html', {'form_user': form_user, 'user_id': user_id})

@login_required
def agregar_a_favoritos(request, id):
    producto = get_object_or_404(Producto, id=id)
    if producto.usuario_favoritos.filter(id=request.user.id).exists():
        producto.usuario_favoritos.remove(request.user)
        messages.success(request, producto.titulo + "Se ha eliminado de tus favoritos")
    else:
        producto.usuario_favoritos.add(request.user)
        messages.success(request, "Se ha agregado el" + producto.titulo + "a favoritos")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def favoritos(request):
    productos = Producto.objects.filter(usuario_favoritos = request.user)

    return render(request, 'account/user/usuario_favoritos.html', {'productos':productos})
