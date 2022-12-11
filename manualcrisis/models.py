from django.db import models

# Create your models here.
class Manual(models.Model): 
    title = models.CharField(max_length=20 , blank= True , null= True )
    file = models.FileField(upload_to= "manualcrisis" , null= True , blank= True)
    dateTimeUploaded = models.DateTimeField(auto_now_add=True)

    deleted_at = models.DateTimeField(
        auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)
    
class Meta:
    verbose_name = "manualcrisis"
    verbose_name_plural = "manualescrisis"
    
    
def __str__(self):
    return self.title