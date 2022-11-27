from django.db import models

# Create your models here.
from django.db import models

from users.models import User
from embed_video.fields  import  EmbedVideoField

# Create your models here.

class test1(models.Model):
    # Relaciones
    # Atributos
    name = models.CharField(max_length=80, verbose_name="name")
    pretest_text =  models.CharField(max_length=400, verbose_name="pretest text", blank=True, null=True)
    introduction_text =  models.CharField(max_length=400, verbose_name="introduction text", blank=True, null=True)
    state_config = models.BooleanField(default=False, verbose_name="config")

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)


    class Meta:
        verbose_name = "test"
        verbose_name_plural = "tests"

    def __str__(self):
        return self.name

class testregister1(models.Model):
    # Relaciones
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(test1, on_delete=models.CASCADE)
    # Atributos
    status = models.BooleanField()
    result_total = models.IntegerField(verbose_name="result_total", blank=True, null=True)
    result_depresion = models.CharField(max_length=200, verbose_name="depresion", blank=True, null=True)
    result_ansiedad = models.CharField(max_length=200, verbose_name="ansiedad", blank=True, null=True)
    result_estres = models.CharField(max_length=200, verbose_name="ansiedad", blank=True, null=True)
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "tests"

    def __str__(self):
        return self.created_at

class question1(models.Model):
    # Relaciones
    test = models.ForeignKey(test1, on_delete=models.CASCADE)
    # Atributos
    question_text = models.CharField(max_length=200, verbose_name="text")
    question_type = models.CharField(max_length=100, verbose_name="type")
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return self.question_text

class alternative1(models.Model):
    # Relaciones
    question = models.ForeignKey(question1, on_delete=models.CASCADE)
    
    # Atributos
    options = {(0),(1),(2),(3)}
    alternative = models.IntegerField(options)
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "alternative"
        verbose_name_plural = "alternative"

    def __str__(self):
        return self.alternative

class respuestas_user1(models.Model):
    # Relaciones
    testregister = models.ForeignKey(testregister1, on_delete=models.CASCADE)
    # Atributos
    options = {(0),(1),(2),(3)}
    alternative = models.IntegerField(options)
    question_text = models.CharField(max_length=200, verbose_name="text")
    question_type = models.CharField(max_length=100, verbose_name="type")
    question_id = models.IntegerField()
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "alternative"
        verbose_name_plural = "alternative"

    def __str__(self):
        return self.alternative

""" Recomendaciones """

class recomendation1(models.Model):
    # Relaciones
    # Atributos
    text_msg =  models.CharField(max_length=600, verbose_name="recomendation text", blank=True, null=True)
    level =  models.CharField(max_length=600, verbose_name="level", blank=True, null=True) # depresion, ansiedad, estres
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)


    class Meta:
        verbose_name = "recomendacion"
        verbose_name_plural = "recomendacion"

    def __str__(self):
        return self.text_msg

class relaxation_techniques1(models.Model):
    # Relaciones
    recomendation = models.ForeignKey(recomendation1, on_delete=models.CASCADE)
    # Atributos
    text_msg =  models.CharField(max_length=600, verbose_name="text", blank=True, null=True)
    level =  models.CharField(max_length=600, verbose_name="level", blank=True, null=True) # normal, severe...
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)
    state_professional = models.BooleanField(default=False, verbose_name="state professional")

    class Meta:
        verbose_name = "tecnica de relajación"
        verbose_name_plural = "tecnicas de relajación"

    def __str__(self):
        return self.text_msg


class link_techniques1(models.Model):
    # Relaciones
    relaxation_techniques = models.ForeignKey(relaxation_techniques1, on_delete=models.CASCADE)
    # Atributos
    text_title =  models.CharField(max_length=600, verbose_name="text title", blank=True, null=True)
    url =  EmbedVideoField()
    autor =  models.CharField(max_length=600, verbose_name="autor", blank=True, null=True)
    canal =  models.CharField(max_length=600, verbose_name="canal", blank=True, null=True)
    origen =  models.CharField(max_length=600, verbose_name="level", blank=True, null=True)
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "url de tecnica"
        verbose_name_plural = "urls de tecnicas"

    def __str__(self):
        return self.text_title




class thermometer_config(models.Model):
    # Relaciones
    # Atributos
    color_1 =  models.CharField(max_length=10, verbose_name="color rgba1", default="#55E659")
    color_2 =  models.CharField(max_length=10, verbose_name="color rgba2", default="#3BB44A")
    color_3 =  models.CharField(max_length=10, verbose_name="color rgba3", default="#FEDA33")
    color_4 =  models.CharField(max_length=10, verbose_name="color rgba4", default="#FC7535")
    color_5 =  models.CharField(max_length=10, verbose_name="color rgba5", default="#EC1B1E")
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)


    class Meta:
        verbose_name = "comfig colors"
        verbose_name_plural = "config colors"

    def __str__(self):
        return self.color_1
