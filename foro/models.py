from django.db import models
from django.conf import settings
from principal.utils import resize_image, decrypt_slug, encrypt_slug
from django.urls import reverse



# Create your models here.

class Foro(models.Model):
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='foro_creator')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='media/')
    slug = models.SlugField(max_length=255)
    creado = models.DateTimeField(auto_now_add=True)
    subido = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, through='principal.Like', related_name='foro_liked')

    def get_absolute_url(self):
        return reverse('foro:foro_publicacion', args=[self.encrypted_slug]) # se le asigna la url que va a mostrar informacion mas detallada del producto

    def save(self, *args, **kwargs):
        # Verifica si el slug ya está generado
        if not self.slug:
            self.slug = encrypt_slug(self.titulo)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.titulo  # O el campo que prefieras mostrar


    @property
    def encrypted_slug(self):
        return encrypt_slug(self.slug)