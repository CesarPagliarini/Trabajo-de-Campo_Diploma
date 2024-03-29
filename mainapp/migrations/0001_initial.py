# Generated by Django 3.0.8 on 2022-07-25 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('habitaciones', '0001_initial'),
        ('huespedes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoEstadia',
            fields=[
                ('nro_estado', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='nro_estado')),
                ('estado', models.CharField(max_length=10, verbose_name='estado')),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
                'db_table': 'estados_estadia',
                'ordering': ['estado'],
            },
        ),
        migrations.CreateModel(
            name='EstadosDecuentos',
            fields=[
                ('nro_estado', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='nro_estado')),
                ('estado', models.CharField(max_length=10, verbose_name='estado')),
            ],
            options={
                'verbose_name': 'Estado Descuento',
                'verbose_name_plural': 'Estados Decuentos',
                'db_table': 'estados_descuento',
                'ordering': ['estado'],
            },
        ),
        migrations.CreateModel(
            name='FormasPago',
            fields=[
                ('id_formaPago', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='id_formaPago')),
                ('descripcion', models.CharField(max_length=10, verbose_name='descripcion')),
            ],
            options={
                'verbose_name': 'FormaPago',
                'verbose_name_plural': 'FormasPago',
                'db_table': 'forma_pago',
                'ordering': ['descripcion'],
            },
        ),
        migrations.CreateModel(
            name='Estadia',
            fields=[
                ('id_estadia', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='id_estadia')),
                ('fecha_inicio', models.DateField(verbose_name='fecha_inicio')),
                ('fecha_fin', models.DateField(blank=True, null=True, verbose_name='fecha_fin')),
                ('cantidad_dias', models.IntegerField(verbose_name='cantidad_dias')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.EstadoEstadia', verbose_name='estado')),
                ('forma_pago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.FormasPago', verbose_name='forma_pago')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habitaciones.Habitacion', verbose_name='habitacion')),
                ('huesped', models.ManyToManyField(to='huespedes.Huesped', verbose_name='Huespedes')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'Estadia',
                'verbose_name_plural': 'Estadias',
                'db_table': 'estadias',
                'ordering': ['id_estadia'],
            },
        ),
        migrations.CreateModel(
            name='Descuentos',
            fields=[
                ('id_descuento', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id_descuento')),
                ('descripcion', models.CharField(max_length=12, verbose_name='descripcion')),
                ('multiplicador', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='multiplicador')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='fecha_creacion')),
                ('fecha_utilizacion', models.DateField(blank=True, editable=False, null=True, verbose_name='fecha_utilizacion')),
                ('estadia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Estadia', verbose_name='estadia')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.EstadosDecuentos', verbose_name='estado')),
            ],
            options={
                'verbose_name': 'Descuento',
                'verbose_name_plural': 'Descuentos',
                'db_table': 'descuentos',
                'ordering': ['id_descuento'],
            },
        ),
    ]
