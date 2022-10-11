from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.

# Create your models here.
class User(AbstractUser):
    # Atributos
    is_client = models.BooleanField(default=False, verbose_name="Cliente")
    is_admin = models.BooleanField(default=False, verbose_name="Admin")
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
 
class userStandard(models.Model):
    # Hereda los campos de tabla user
    user= models.OneToOneField(User, on_delete=models.CASCADE)
 
    # Atributos
    matricula = models.CharField(max_length=12, verbose_name="matricula")
    phone = models.CharField(max_length=15, verbose_name="telefono")
    sexo = models.CharField(max_length=15, verbose_name="sexo", blank=True, null=True)

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "userStandard"
        verbose_name_plural = "userStandard"

    def __str__(self):
        return self.user.username