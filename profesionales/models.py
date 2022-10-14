from django.db import models

# Create your models here.
# Create your models here.
class Profesional(models.Model):
    imagen_profesional = models.ImageField(upload_to="profesional",null=True)
    nombre = models.CharField(max_length=100,verbose_name='Nombre',blank=True,null=True)
    apellido = models.CharField(max_length=100,verbose_name='Apellido',blank=True,null=True)
    curp = models.CharField(max_length=20,verbose_name='CURP')
    correo = models.EmailField(max_length=300,blank=True,null=True)
    numero_1 = models.IntegerField(max_length=15,blank=True,null=True)
    numero_2 = models.IntegerField(max_length=15,blank=True,null=True)
    redes = models.CharField(max_length=300,blank=True,null=True)
    ubicacion = models.CharField(max_length=500,blank=True,null=True)
    especialidades = models.CharField(max_length=500,blank=True,null=True)
    servicios = models.CharField(max_length=300, blank=True,null=True)
    valor = models.IntegerField(max_length=15,blank=True,null=True)

class Meta:
    verbose_name = 'Profesional'
    verbose_name_plural = 'Profesionales'

def __str__(self):
    return str(self.curp)