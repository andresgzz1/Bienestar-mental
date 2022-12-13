from django.db import models
from users.models import User


class Manual(models.Model):

    titulo = models.CharField(max_length=20, verbose_name="title")
    subirPDF = models.FileField(upload_to="PDF/", null=True, blank=True)
    dateTimeSubida = models.DateTimeField(auto_now_add=True)

    deleted_at = models.DateTimeField(
        auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)


class Meta:
    verbose_name = "manual"
    verbose_name_plural = "manuales"


def __str__(self):
    return self.titulo
# Create your models here.
