# Generated by Django 3.2.16 on 2022-11-25 00:34

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('diario_emocional', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='emocion',
            field=models.CharField(max_length=30, verbose_name=users.models.User),
        ),
    ]