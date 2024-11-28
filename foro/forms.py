from django import forms
from principal.models import Comentario
from .models import Foro

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['campo']
        
    def __init__(self, *args, **kwargs):
        super(ComentarioForm, self).__init__(*args, **kwargs)

class ForoForm(forms.ModelForm):
    class Meta:
        model = Foro
        fields = ['titulo','descripcion','imagen','slug']

    slug = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))


    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        if len(titulo) < 5 or len(titulo) > 50:
            raise forms.ValidationError("El título debe tener entre 5 y 50 caracteres.")
        return titulo
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Foro.objects.filter(slug=slug).exists():
            raise forms.ValidationError("El slug debe ser único.")
        return slug
    
    def __init__(self, *args, **kwargs):
        super(ForoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class EditarForo(forms.ModelForm):
    class Meta:
        model = Foro
        fields = ('titulo', 'descripcion', 'imagen')
        widgets={
            'titulo': forms.TextInput(attrs={
                'class':'form-control',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'imagen': forms.FileInput(attrs={
                'class':'form-control',               
            }),                
        }