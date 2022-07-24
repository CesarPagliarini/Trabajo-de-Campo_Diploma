# Generated by Django 3.0.8 on 2022-07-23 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoHabitacion',
            fields=[
                ('id_tipo_habitacion', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='id_tipo_habitacion')),
                ('nombre', models.CharField(max_length=12, verbose_name='nombre')),
                ('capacidad', models.IntegerField(verbose_name='capacidad')),
                ('superficie', models.IntegerField(verbose_name='superficie')),
                ('cantidad_ambientes', models.IntegerField(verbose_name='superficie')),
                ('cantidad_banos', models.IntegerField(verbose_name='cantidad_banos')),
                ('precio_por_noche', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='precio_por_noche')),
            ],
            options={
                'verbose_name': 'Tipo de habitacion',
                'verbose_name_plural': 'Tipos de habitaciones',
                'db_table': 'tipo_habitaciones',
            },
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('nro_habitacion', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='nro_habitacion')),
                ('estado', models.CharField(max_length=10, verbose_name='estado')),
                ('tipo_habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habitaciones.TipoHabitacion', verbose_name='tipo_habitacion')),
            ],
            options={
                'verbose_name': 'Habitacion',
                'verbose_name_plural': 'Habitaciones',
                'db_table': 'habitaciones',
            },
        ),
    ]