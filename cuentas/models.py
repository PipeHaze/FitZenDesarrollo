import uuid
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_superuser(self,email, user_name, password, **other_fields):
        """
        @create_superuser es para crear a un superusuario
        revisa si es administrador(is_staff),
               si es superusuario (is_superuser)
               si esta activo.

        la funcion requiere 3 parametros, **otherfields ignora los demas argumentos;
        estos son correo, nombre de usuario y contraseña, si el formulario es llenado de manera
        exitosa retorna el usuario creado.
        """

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'El Superusuario debe estar asignado a is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'El Superusuario debe estar asignado a is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)
    
    def create_user(self, email, user_name, password, **other_fields):
        
        """
        funcion create_user():
        para crear un usuario se requiere el correo electronico, nombre de usuario
        y contraseña, ignora los demas datos con **other_fields.

        si el correo electronico no es llenado en el formulario saldra un mensaje que este campo es
        necesario.(Debes ingresar un correo electronico).

        al llenar los datos, la variable user va a contener los campos del modelo UserBase,
        para ir almacenando los usuarios creados.
        """

        if not email:
            raise ValueError(_('Debes ingresar un correo electronico'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user
    
class UserBase(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('Ingresa tu correo'),unique=True)
    user_name = models.CharField(max_length=150, unique=True) #user_name
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_(
        'acerca_de'),max_length=500, blank= True)
    #estado de usuario
    is_active = models.BooleanField(default=False)#usuario esta activo o inactivo
    is_staff = models.BooleanField(default= False)
    creado = models.DateTimeField(auto_now_add=True) #tipo de dato era created pero yo no soy gringo
    modificado = models.DateTimeField(auto_now= True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        """
        subject y mesage son los campos y el contenido del correo electronico del destinatario
        self.email es la funcion de django que permite mandar correos.
        
        """

        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.user_name    
    