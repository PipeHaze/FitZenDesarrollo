from django import forms
from django.contrib.auth.forms import(AuthenticationForm, PasswordResetForm, SetPasswordForm)
from django.forms.widgets import FileInput
from .models import UserBase
from django.contrib.auth.forms import UserChangeForm

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Ingresa Tu Correo', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'login-pwd',
        }
    ))

class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        min_length = 6, max_length = 15,
        help_text = 'Requerido',
        widget=forms.TextInput(attrs={'pattern': '^[A-Z][a-zA-Z]{6,15}$'}),
        error_messages = {
            'Requerido': 'Debes ingresar un nombre de usuario'
        }

    )

    email = forms.EmailField(max_length = 100, help_text = 'Requerido', error_messages = {
        'Requerido': 'Ingresa un email valido'})
    
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput,
        min_length = 6, max_length = 15,
        error_messages = {
            'Requerido': 'La contraseña debe tener un largo de 6 a 15 caracteres'},
    )
    
    password2 = forms.CharField(label = 'Confirma contraseña', widget = forms.PasswordInput,
        min_length = 6, max_length = 15,
        error_messages = {
            'Requerido': 'La contraseña debe tener un largo de 6 a 15 caracteres'},
    )

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name = user_name)#verifica si hay usuarios con el mismo nombre, lo cual no esta permitido
        if r.count():
            raise forms.ValidationError("El usuario ya existe")
        return user_name
    
    def clean_password2(self):
        cd = self.cleaned_data #cd = cleaned_data
        if cd['password'] != cd['password2']: #comprobar si las contraseñas coinciden, ! significa diferencia
            raise forms.ValidationError('Contraseñas no coinciden')
        return cd['password2'] #si las contraseñas no coinciden, se borran del formulario de registro
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email = email).exists(): # no pueden haber 2 personas con el mismo correo
            raise forms.ValidationError(
                'Ingresa otro correo, este ya esta en uso.')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Nombre de Usuario'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Ingresa tu Correo', 'name': 'email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirma contraseña'})
        
class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254,widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Hubo un error al encontrar tu correo electronico')
        return email
    
class PwdResetConfirmForm(SetPasswordForm): #formulario para cambio de contraseña
    new_password1 = forms.CharField(
        label='Nueva contraseña', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Nueva contraseña', 'id': 'form-newpass'}))

    new_password2 = forms.CharField(
        label='Repite contraseña', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Nueva contraseña', 'id': 'form-new-pass2'}))
    

