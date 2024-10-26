import uuid
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
class Direccion(models.Model):
    """
    Direcciones
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable= False)
    usuario = models.ForeignKey(UserBase, verbose_name=("usuario"), on_delete=models.CASCADE)
    nombre_completo = models.CharField(_("Nombre Completo"), max_length=150)
    pais = CountryField()
    telefono = models.CharField(max_length=15, blank= True)
    codigopostal = models.CharField(max_length=12,blank= True)
    direccion_1 = models.CharField(max_length=150, blank= True)        
    direccion_2 = models.CharField(max_length=150, blank= True)
    comuna = models.CharField(max_length=150, blank= True)
    instrucciones_delivery = models.CharField(_("Instrucciones delivery"), max_length=255)
    creado_en = models.DateTimeField(("Creado en"), auto_now_add=True)
    modificado_en = models.DateTimeField(_("Modificado en"), auto_now_add=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Direccion"
        verbose_name_plural = "Direcciones"

    def __str__(self):
        return "Direccion"
    

class Perfil(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=250)
    imagen_perfil = models.ImageField(default='media/default.jpg', upload_to='media', null=True)
    direccion_user = models. TextField(max_length="50", null=True)
    telefono = models.TextField(max_length=50,null=True)
    tipo_trabajo = models.TextField(max_length=70, null=True)
    cargo_trabajo = models.TextField(max_length=60)

    def __str__(self):
        return f"{self.user.email} Perfil"

@receiver(post_save, sender=UserBase)
def crear_perfil_al_crear_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance, descripcion='Descripción predeterminada')

    