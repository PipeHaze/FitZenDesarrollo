# Generated by Django 4.2.16 on 2024-11-27 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('principal', '0006_comentario_comentario_padre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('contenido', models.TextField()),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicaciones', to='principal.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicaciones', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Publicaciones',
                'ordering': ['-creado_en'],
            },
        ),
    ]
