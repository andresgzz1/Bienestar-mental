# Generated by Django 3.2.16 on 2022-11-14 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_emocional', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Diario',
            new_name='Entrada',
        ),
    ]
