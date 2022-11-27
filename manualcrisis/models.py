from django.db import models

# Create your models here.
class Manual(models.Model): 
    title = models.CharField(max_length=20 , blank= True , null= True )
    file = models.FileField(upload_to= "manualcrisis" , null= True , blank= True)
    
    
    
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha ingreso")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)
    
    
def __str__(self):
    return self.title