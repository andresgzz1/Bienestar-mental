from django.db import models
from users.models import User

# Create your models here.


class avisosPrivacidad(models.Model):

    title = models.CharField(max_length=20, verbose_name="title")
    uploadPDF = models.FileField(
        upload_to="avPrivacidad/", null=True, blank=True)
    dateTimeUploaded = models.DateTimeField(auto_now_add=True)

    deleted_at = models.DateTimeField(
        auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)


class Meta:
    verbose_name = "avisosPrivacidad"


def __str__(self):
    return self.title
# Create your models here.
