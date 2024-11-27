from django import forms
from .models import Categoria, Producto, Comentario


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
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Producto.objects.filter(slug=slug).exists():
            raise forms.ValidationError("El slug debe ser único.")
        return slug
    
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['campo']
        
    def __init__(self, *args, **kwargs):
        super(ComentarioForm, self).__init__(*args, **kwargs)

class EditarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('titulo', 'descripcion', 'precio', 'imagen','categoria')
        widgets={
            'titulo': forms.TextInput(attrs={
                'class':'form-control',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'precio': forms.TextInput(attrs={
                'class':'form-control',
                'type': 'number'
            }),
            'imagen': forms.FileInput(attrs={
                'class':'form-control',
                
            }),
            'categoria': forms.RadioSelect(attrs={
                'class': 'form-check-label'

            }),
                
        }

