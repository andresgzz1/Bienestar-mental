from django.db import models
from users.models import User


class termsCondition(models.Model):

    title = models.CharField(max_length=20, verbose_name="title")
    uploadPDF = models.FileField(
        upload_to="PDF/", null=True, blank=True)
    dateTimeUploaded = models.DateTimeField(auto_now_add=True)

    deleted_at = models.DateTimeField(
        auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)


class Meta:
    verbose_name = "termsCondition"
    verbose_name_plural = "termsConditions"


def __str__(self):
    return self.title
# Create your models here.
