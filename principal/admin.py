from django.contrib import admin
from .models import Categoria, Producto, ForoProducto, Like

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

@admin.register(ForoProducto)
class ForoProductoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'producto']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['foro_producto']

