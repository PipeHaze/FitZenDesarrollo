from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique= True)

    class Meta:
        verbose_name_plural = 'categorias'

    def get_absolute_url(self):
        return reverse('tiendita:categoria_lista', args=[self.slug])

    def __str__(self):
        return self.nombre