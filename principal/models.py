from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from principal.utils import resize_image, decrypt_slug, encrypt_slug

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager,self).get_queryset().filter(activo=True)

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique= True)

    class Meta:
        verbose_name_plural = 'categorias'

    def get_absolute_url(self):
        return reverse('principal:categoria_lista', args=[self.slug])

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='producto',on_delete=models.CASCADE)
    #creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, default='admin')
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='media/')
    slug = models.SlugField(max_length=255)
    precio = models.DecimalField(max_digits=7, decimal_places=3)
    en_stock = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    subido = models.DateTimeField(auto_now=True)
    aprobado = models.BooleanField(default= False) # pasara a ser revisado para mostrase con los demas productos
    stock = models.IntegerField()
    objects = models.Manager()
    producto = ProductManager()

    class Meta:
        verbose_name_plural = 'Productos'
        ordering = ('-creado',)

    def get_absolute_url(self):
        return reverse('principal:informacion_productos', args=[self.encrypted_slug]) # se le asigna la url que va a mostrar informacion mas detallada del producto
    
    def save(self, *args, **kwargs):
    # Redimensionar la imagen antes de guardarla
        if self.imagen:
            resize_image(self.imagen)

    # Verifica si el slug ya está generado
        if not self.slug:
            self.slug = encrypt_slug(self.titulo)
            print(f"Slug generado: {self.slug}")  # Depuración del slug

        super().save(*args, **kwargs)  # Asegúrate de que se guarde correctamente en la BD
        print(f"Producto guardado con ID: {self.id}")  # Verificar que se guarda correctamente

    def __str__(self):
        return self.titulo
    
    @property
    def encrypted_slug(self):
        return encrypt_slug(self.slug)