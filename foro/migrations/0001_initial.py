# Generated by Django 4.2.16 on 2024-11-28 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('principal', '0008_delete_publicacion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Foro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('imagen', models.ImageField(upload_to='media/')),
                ('slug', models.SlugField(max_length=255)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('subido', models.DateTimeField(auto_now=True)),
                ('creado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foro_creator', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(related_name='foro_liked', through='principal.Like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]