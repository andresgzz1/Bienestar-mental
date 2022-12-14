# Generated by Django 3.2.16 on 2022-11-28 15:47

from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_space', models.ImageField(blank=True, null=True, upload_to='space', verbose_name='dir image')),
                ('space_name', models.CharField(max_length=100, verbose_name='name space')),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha ingreso')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
            ],
        ),
        migrations.CreateModel(
            name='music_space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_music', models.CharField(max_length=100, verbose_name='name music')),
                ('music_space', models.FileField(blank=True, null=True, upload_to='space')),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha ingreso')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relaxation_space.space', verbose_name='space')),
            ],
        ),
        migrations.CreateModel(
            name='image_space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_image', models.CharField(max_length=100, verbose_name='name image')),
                ('img_space', models.ImageField(blank=True, null=True, upload_to='space', verbose_name='dir image')),
                ('image_url', embed_video.fields.EmbedVideoField()),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha ingreso')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relaxation_space.space', verbose_name='space')),
            ],
        ),
        migrations.CreateModel(
            name='gif_space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_gif', models.CharField(max_length=100, verbose_name='name gif')),
                ('gif_space', models.FileField(blank=True, null=True, upload_to='space')),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha ingreso')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relaxation_space.space', verbose_name='space')),
            ],
        ),
    ]
