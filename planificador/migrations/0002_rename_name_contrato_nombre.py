# Generated by Django 4.2.11 on 2024-05-08 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planificador', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contrato',
            old_name='name',
            new_name='nombre',
        ),
    ]
