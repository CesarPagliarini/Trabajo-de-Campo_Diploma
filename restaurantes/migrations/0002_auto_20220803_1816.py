# Generated by Django 3.2.14 on 2022-08-03 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TurnosReserva',
            new_name='TurnoReserva',
        ),
        migrations.AlterModelOptions(
            name='estadoreservarestaurante',
            options={'verbose_name': 'Estado Reserva Restaurante', 'verbose_name_plural': 'Estados Reservas Restaurantes'},
        ),
        migrations.AlterModelOptions(
            name='reservarestaurante',
            options={'verbose_name': 'Reserva Restaurante', 'verbose_name_plural': 'Reservas Restaurantes'},
        ),
        migrations.AlterModelOptions(
            name='restaurante',
            options={'verbose_name': 'Restaurante', 'verbose_name_plural': 'Restaurantes'},
        ),
        migrations.AlterModelOptions(
            name='tiporestaurante',
            options={'verbose_name': 'Tipo Restaurante', 'verbose_name_plural': 'Tipos Restaurantes'},
        ),
        migrations.AlterModelOptions(
            name='turnoreserva',
            options={'verbose_name': 'Turno Reserva', 'verbose_name_plural': 'Turnos Reservas'},
        ),
        migrations.AlterModelTable(
            name='estadoreservarestaurante',
            table='estado_reserva_restaurante',
        ),
        migrations.AlterModelTable(
            name='reservarestaurante',
            table='reservas_restaurantes',
        ),
        migrations.AlterModelTable(
            name='restaurante',
            table='restaurantes',
        ),
        migrations.AlterModelTable(
            name='tiporestaurante',
            table='tipo_restaurante',
        ),
        migrations.AlterModelTable(
            name='turnoreserva',
            table='turnos_reservas',
        ),
    ]
