from django.shortcuts import render, redirect
from .forms import RegistrationForm,UserEditForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserBase
from django.contrib.auth import login, logout
from .token import account_activation_token
from django.contrib.auth.decorators import login_required
from pedidos.views import pedido_usuarios




# Create your views here.

def registro_usuarios(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit = False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False #el usuario tiene que activarse.
            user.save()
            #configurar email
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta'
            message = render_to_string('account/registration/account_activation_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user), #se le tiene que asignar el token, se crea con token.py y agregar aqui.
            })
            user.email_user(subject = subject, message = message) #en el terminal se muestra esto
            return HttpResponse('Registro exitoso, se ha enviado la activacion.')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/registro.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    "funcion que muestra el mensaje para activar la cuenta"
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk = uid)
    except(TypeError):
        pass
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('principal:paginaprincipal')
    else:
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

    
