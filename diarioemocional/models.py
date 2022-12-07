from django.db import models
from users.models import User


# Create your models here.

class Emocion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    imagen_emocion = models.ImageField(upload_to="emocion",null=True, blank=True)
    nombre = models.CharField(max_length=100,blank=True,null=True)

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "emocion"
        verbose_name_plural = "emociones"

    def __str__(self):
        return self.nombre

class Entrada(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    img_emocion = models.ImageField(upload_to="emocion",null=True, blank=True)
    emocion = models.CharField(User,max_length=30)
    descripcion = models.CharField(max_length=1000,blank=True,null=True)

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)