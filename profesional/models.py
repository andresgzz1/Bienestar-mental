from django.db import models
from users.models import User

# Create your models here.
class Profesional(models.Model):
    imagen_profesional = models.ImageField(upload_to="profesional",null=True, blank=True)
    nombre = models.CharField(max_length=100,verbose_name='Nombre')
    apellido = models.CharField(max_length=100,verbose_name='Apellido')
    curp = models.CharField(max_length=20,verbose_name='CURP')
    correo = models.EmailField(max_length=300,blank=True,null=True)
    numero_1 = models.IntegerField(blank=True,null=True)
    numero_2 = models.IntegerField(blank=True,null=True)
    redes = models.CharField(max_length=300,blank=True,null=True)
    ubicacion = models.CharField(max_length=500,blank=True,null=True)
    especialidades = models.CharField(max_length=500,blank=True,null=True)
    servicios = models.CharField(max_length=300, blank=True,null=True)
    valor = models.IntegerField(blank=True,null=True)

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha ingreso")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

class Meta:
    verbose_name = 'Profesional'
    verbose_name_plural = 'Profesionales'

def __str__(self):
    return self.curp