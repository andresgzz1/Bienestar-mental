# Generated by Django 3.2.16 on 2022-11-28 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relaxation_space', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image_space',
            name='image_url',
        ),
    ]