from django.db import models

# Create your models here.


class infoOrg(models.Model):

    # Atributos
    long_name = models.CharField(max_length=100, verbose_name="long name")
    short_name = models.CharField(max_length=20, verbose_name="short name")
    description = models.CharField(max_length=300, verbose_name="description")
    color_1 = models.CharField(max_length=10, verbose_name="color 1")
    color_2 = models.CharField(max_length=10, verbose_name="color 2")
    color_3 = models.CharField(max_length=10, verbose_name="color 3")
    
    
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "info org"
        verbose_name_plural = "info org"

    def __str__(self):
        return self.long_name