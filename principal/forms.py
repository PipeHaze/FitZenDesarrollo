from django import forms
from .models import Categoria, Producto


class ProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    class Meta:
        model = Producto
        fields = ['titulo', 'descripcion', 'imagen', 'precio','stock', 'slug']

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio
    
    def punto_precio(self):
        precio = self.cleaned_data['precio']
        # Verifica si el precio contiene un punto decimal
        if '.' not in str(precio):
            raise forms.ValidationError('El precio debe contener un punto decimal.')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock
    
    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        if len(titulo) < 5 or len(titulo) > 50:
            raise forms.ValidationError("El título debe tener entre 5 y 50 caracteres.")
        return titulo