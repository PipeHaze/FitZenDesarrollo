# Generated by Django 4.2.16 on 2024-10-11 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('principal', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=50)),
                ('direccion1', models.CharField(max_length=250)),
                ('direccion2', models.CharField(max_length=250)),
                ('ciudad', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
                ('codigo_postal', models.CharField(max_length=20)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('total_pagado', models.DecimalField(decimal_places=3, max_digits=7)),
                ('pedido_key', models.CharField(max_length=200)),
                ('estado_factura', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-creado',),
            },
        ),
        migrations.CreateModel(
            name='PedidoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=3, max_digits=7)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pedidos.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_items', to='principal.producto')),
            ],
        ),
    ]