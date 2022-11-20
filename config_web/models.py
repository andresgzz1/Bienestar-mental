from django.db import models


class termsCondition(models.Model):

    title = models.CharField(max_length=20, verbose_name="title")
    uploadFile = models.FileField(upload_to="Uploaded Files/")
    dateTimeUploaded = models.DateTimeField(auto_now_add=True)

    deleted_at = models.DateTimeField(
        auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)


class Meta:
    verbose_name = "termsCondition"
    verbose_name_plural = "termsConditions"


def __str__(self):
    return self.title
# Create your models here.
