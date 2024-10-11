from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserBase
from django.contrib.auth import login, logout
from .token import account_activation_token



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
