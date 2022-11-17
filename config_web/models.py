from django.db import models



class termsCondition(models.Model):
    
    title = models.CharField(max_length=20, verbose_name="title")
    body_text = models.TextField(verbose_name="body_text", blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

class Meta:
    verbose_name = "termsCondition"
    verbose_name_plural = "termsConditions"

def __str__(self):
    return self.title
# Create your models here.
