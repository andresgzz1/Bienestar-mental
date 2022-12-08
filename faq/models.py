from django.db import models

# Create your models here.

class faq(models.Model):
    # Hereda los campos de tablas

    # Atributos
    question = models.CharField(
        max_length=250, verbose_name="question", default="")
    resp = models.CharField(max_length=400, verbose_name="telefono")
    type = models.CharField(max_length=20, verbose_name="tipo") # depresion/ansiedad/estres/web
    state = models.BooleanField()
    
    # Info del registro
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at = models.DateTimeField(
        auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "faq"
        verbose_name_plural = "faqs"

    def __str__(self):
        return self.question