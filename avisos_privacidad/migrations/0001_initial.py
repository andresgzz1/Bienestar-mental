# Generated by Django 3.2.16 on 2022-12-13 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='avisosPrivacidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='title')),
                ('uploadPDF', models.FileField(blank=True, null=True, upload_to='avPrivacidad/')),
                ('dateTimeUploaded', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
            ],
        ),
    ]
