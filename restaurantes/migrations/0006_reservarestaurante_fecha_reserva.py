# Generated by Django 3.2.14 on 2022-08-04 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantes', '0005_auto_20220804_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservarestaurante',
            name='fecha_reserva',
            field=models.DateField(default='2022-08-03', verbose_name='fecha_reserva'),
        ),
    ]