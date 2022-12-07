from django.db import models
from embed_video.fields  import  EmbedVideoField
# Create your models here.


""" Tabla Espacio de relajación (lluvia, cafetería, playa, noche, viento)  """
# Create your models here.
class space(models.Model):
    img_space = models.ImageField(upload_to="space",null=True, blank=True, verbose_name='dir image')
    space_name = models.CharField(max_length=100,verbose_name='name space')
    state = models.BooleanField(default=True, verbose_name="state")

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha ingreso")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

def __str__(self):
    return self.space_name


""" Imagenes de los espacios de relajación  """
class image_space(models.Model):
    space = models.ForeignKey(space, on_delete=models.CASCADE, verbose_name="space")
    name_image = models.CharField(max_length=100,verbose_name='name image')
    space_img = models.ImageField(upload_to="relaxation_space",null=True, blank=True, verbose_name='space image')
    state = models.BooleanField(default=True, verbose_name="state")

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha ingreso")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

""" Musica de los espacios de relajación  """
class sound_space(models.Model):
    space = models.ForeignKey(space, on_delete=models.CASCADE, verbose_name="space")
    name_music = models.CharField(max_length=100,verbose_name='name music')
    music_space = models.FileField(upload_to="space",null=True, blank=True)
    state = models.BooleanField(default=True, verbose_name="state")

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha ingreso")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

""" Gifs de los espacios de relajación  """
class gif_space(models.Model):
    space = models.ForeignKey(space, on_delete=models.CASCADE, verbose_name="space")
    name_gif = models.CharField(max_length=100,verbose_name='name gif')
    gif_space = models.ImageField(upload_to="space",null=True, blank=True)
    state = models.BooleanField(default=True, verbose_name="state")

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha ingreso")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)
