# Generated by Django 3.2.16 on 2022-11-28 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config_web', '0003_rename_uploadfile_termscondition_uploadpdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termscondition',
            name='uploadPDF',
            field=models.FileField(blank=True, null=True, upload_to='PDF/'),
        ),
    ]
