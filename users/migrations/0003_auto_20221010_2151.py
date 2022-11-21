# Generated by Django 3.2.16 on 2022-10-11 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userstandard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstandard',
            name='rut',
        ),
        migrations.AddField(
            model_name='userstandard',
            name='matricula',
            field=models.CharField(default=10, max_length=12, verbose_name='matricula'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userstandard',
            name='sexo',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='sexo'),
        ),
        migrations.AlterField(
            model_name='userstandard',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='telefono'),
        ),
    ]
