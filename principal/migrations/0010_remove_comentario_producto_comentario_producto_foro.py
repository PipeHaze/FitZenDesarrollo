# Generated by Django 4.2.16 on 2024-11-28 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foro', '0001_initial'),
        ('principal', '0009_alter_like_unique_together_like_foro_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='producto',
        ),
        migrations.AddField(
            model_name='comentario',
            name='producto_foro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='foro.foro'),
        ),
    ]
