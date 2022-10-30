from pickle import FALSE
from turtle import update
from unicodedata import name
from django.shortcuts import render, redirect
import profesional
from questionnaire.models import Alternative, Question, Respuestas_user, Test, TestRegister
from profesional.models import Profesional
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
import re


# Create your views here.

# Validación de correo
def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None

def valid_extension(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and 
        not value.name.endswith('.gif') and
        not value.name.endswith('.bmp') and 
        not value.name.endswith('.jpg')):
        raise ValidationError("Error al subir imagen, no corresponde a uno de las extensiones permitidas: .jpg, .jpeg, .png, .gif, .bmp")


# Templates Render


@login_required()
def indexViewProfesional(request):
    user = request.user
    if user.isauthenticated:
        if user.is_admin:
            return render(request, 'createProfesional.html')
        else:
            return redirect('login2')
    else:
        return redirect('login2')

@login_required()
def indexCreateProfesional(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'createProfesional.html')
    else:
        return redirect('login2')

# Endpoint
def get_All_Profesional(request, format=None):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            profesional = Profesional.objects.all()
            contexto = {'profesional':profesional}
            return render(request, 'administradorProfesionales.html', contexto)
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

def get_Profesional(request, idProfesional):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            profesional = Profesional.objects.get(pk=idProfesional)
            contexto = {'profesional':profesional}
            return render(request, 'administradorProfesionales.html', contexto)
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

def addProfesional(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            global profesional
            foto = request.FILES['Imagen']
            nombre = request.POST['Nombre']
            if isinstance(nombre,int):
                return Response({'Msj':'Error, el nombre debe contener letras, no números'})
            apellido = request.POST['Apellido']
            if isinstance(apellido,int):
                return Response({'Msj':'Error, el apellido debe contener letras, no números'})
            correo = request.POST['Correo']
            numero_1 = request.POST['Número 1']
            numero_2 = request.POST['Número 2']
            redes = request.POST['Redes']
            ubicacion = request.POST['Ubicación']
            especialidades = request.POST['Especialidades']
            servicios_valor = request.POST['Servicios y valor']
            horario_laboral = request.POST['Horario laboral']
            redirectUrl = ''
            h_list_array = Profesional.objects.order_by('nombre')
            if nombre == '' or apellido == '':
                messages.add_message(request=request, level = messages.ERROR, message="No ha ingresado un campo requerido")
                return render(request, 'createProfesional.html', {"profesional" : profesional})
            if correo != '' and es_correo_valido(correo) == False:
                messages.add_message(request=request, level = messages.ERROR, message="Ha ingresado un correo inválido")
                return render(request, 'createProfesional.html', {"profesional" : profesional})
            else:
                try:
                    profesional = Profesional.objects.create(
                        imagen_profesional = foto,
                        nombre = nombre,
                        apellido = apellido,
                        correo = correo,
                        numero_1 = numero_1,
                        numero_2 = numero_2,
                        redes = redes,
                        ubicacion = ubicacion,
                        especialidades = especialidades,
                        servicios_valor = servicios_valor,
                        horario_laboral = horario_laboral
                    )
                    messages.add_message(request=request, level = messages.SUCCESS, message="Profesional agregado correctamente")
                    redirect('pageadmin')
                except Exception as e:
                    messages.add_message(request = request, level = messages.ERROR,message="Ha ocurrido un error al agregar al profesional")
                    redirect('customer')
            return redirect('pageadmin')
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('login2')
    else:
        return redirect('login2')

def updateProfesional(request, idProfesional):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            #foto = request.FILES['Imagen']
            nombre = request.POST['Nombre']
            if isinstance(nombre,int):
                return Response({'Msj':'Error, el nombre debe contener letras, no números'})
            apellido = request.POST['Apellido']
            if isinstance(apellido, int):
                return Response({'Msj':'Error, el apellido debe contener letras, no números'})
            correo = request.POST['Correo']
            numero_1 = request.POST['Número 1']
            numero_2 = request.POST['Número 2']
            redes = request.POST['Redes']
            ubicacion = request.POST['Ubicación']
            especialidades = request.POST['Especialidades']
            servicios_valor = request.POST['Servicios y valor']
            redirectUrl = ''
            profesional = Profesional.objects.get(id=idProfesional)
            if nombre == '' or apellido == '':
                messages.add_message(request=request, level = messages.SUCCESS, message="El Nombre es un campo requerido")
                return render(request, 'updateProfesional.html', {"profesional" : profesional} )
            else:
                try:
                    #profesional.imagen_profesional = foto
                    profesional.nombre = nombre
                    profesional.apellido = apellido
                    profesional.correo = correo
                    profesional.numero_1 = numero_1
                    profesional.numero_2 = numero_2
                    profesional.redes = redes
                    profesional.ubicacion = ubicacion
                    profesional.especialidades = especialidades
                    profesional.servicios_valor = servicios_valor
                    profesional.horario_laboral
                    profesional.save()
                    messages.add_message(request=request, level = messages.SUCCESS, message="Profesional editado correctamente")
                    return redirect('get_All_Profesional')
                except Exception as e:
                    messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al editar al profesional")
                    return render(request, 'updateProfesional.html', {"profesional" : profesional} )
                return redirect(redirectUrl)
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

@login_required()
def indexUpdateProfesional(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if Profesional.objects.filter().exists():
                firstProfesional = Profesional.objects.filter()[:1].get()
                profesional = Profesional.objects.get(id=firstProfesional.id)
                msg = "Profesional Configurado"
                profesional.save()
                return render(request, 'updateProfesional.html', {"profesional" : profesional, "msgGood":msg} )  
            else:
                profesionalprimary = Profesional.objects.create(
                )
                messages.add_message(request=request, level = messages.SUCCESS, message="Por favor, vuelve a ingresar al area de 'profesional'")
                return redirect('pageadmin')
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

@login_required
def deleteProfesional(request, idProfesional):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if Profesional.objects.filter(id=idProfesional).exists():
                Profesional.objects.filter(pk=idProfesional).delete()
                messages.add_message(request=request, level = messages.SUCCESS, message="Profesional eliminado correctamente")
                return redirect('pageadmin')
            else:
                messages.add_message(request=request, level = messages.ERROR, message="No existe el profesional")
                return redirect('pageadmin')
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

def editarProfesional(request, idProfesional):
    profesional = Profesional.objects.get(pk=idProfesional)
    return render(request, "updateProfesional.html", {"profesional":profesional})

def detalleProfesional(request, idProfesional):
    profesional = Profesional.objects.get(pk=idProfesional)
    return render(request, "detalleProfesional.html", {"profesional":profesional})