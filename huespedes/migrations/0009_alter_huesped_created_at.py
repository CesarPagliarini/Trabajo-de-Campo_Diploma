# Generated by Django 3.2.14 on 2022-08-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('huespedes', '0008_huesped_user_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='huesped',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Creado'),
        ),
    ]
