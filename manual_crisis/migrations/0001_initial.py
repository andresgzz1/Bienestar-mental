# Generated by Django 3.2.16 on 2022-12-11 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=20, verbose_name='title')),
                ('subirPDF', models.FileField(blank=True, null=True, upload_to='PDF/')),
                ('dateTimeSubida', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
            ],
        ),
    ]
