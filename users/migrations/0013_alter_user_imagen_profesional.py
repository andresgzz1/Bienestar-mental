# Generated by Django 3.2.16 on 2022-11-16 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_user_imagen_profesional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='imagen_profesional',
            field=models.ImageField(blank=True, null=True, upload_to='users'),
        ),
    ]
