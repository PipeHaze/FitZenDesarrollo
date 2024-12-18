from django.contrib import admin
from .models import Categoria, Producto, Like, Comentario

# Register your models here.
# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'slug', 'precio',
                    'en_stock', 'creado', 'subido']
    list_filter = ['en_stock', 'activo']
    list_editable = ['precio', 'en_stock']
    prepopulated_fields = {'slug': ('titulo',)}

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'campo']





