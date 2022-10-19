from django.db import models

from users.models import User

# Create your models here.

class Test(models.Model):
    # Relaciones
    # Atributos
    name = models.CharField(max_length=80, verbose_name="name")
    pretest_text =  models.CharField(max_length=400, verbose_name="pretest text", blank=True, null=True)
    introduction_text =  models.CharField(max_length=400, verbose_name="introduction text", blank=True, null=True)

    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "tests"

    def __str__(self):
        return self.name

class TestRegister(models.Model):
    # Relaciones
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    # Atributos
    status = models.BooleanField()
    result_depresion = models.CharField(max_length=200, verbose_name="depresion", blank=True, null=True)
    result_ansiedad = models.CharField(max_length=200, verbose_name="ansiedad", blank=True, null=True)
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "tests"

    def __str__(self):
        return self.created_at

class Question(models.Model):
    # Relaciones
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
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

class Alternative(models.Model):
    # Relaciones
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
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
        return self.alernative

class Respuestas_user(models.Model):
    # Relaciones
    testregister = models.ForeignKey(TestRegister, on_delete=models.CASCADE)
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
        return self.alernative
