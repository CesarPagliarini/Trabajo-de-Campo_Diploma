# Generated by Django 3.2.14 on 2022-08-08 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auditoria', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actividadusuario',
            options={'ordering': ['creado'], 'verbose_name': 'Actividad', 'verbose_name_plural': 'Actividades'},
        ),
    ]