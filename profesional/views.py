from pickle import FALSE
from unicodedata import name
from django.shortcuts import render, redirect
from profesional.models import Profesional
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re


# Create your views here.

# Validación de correo
def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None

# Endpoint
@api_view(['GET'])
def get_All_Profesional(request, format=None):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            try:
                prof_list = Profesional.objects.all()
                prof_json=[]
                for h in prof_list:
                    prof_json.append({'nombre':h.nombre, 'apellido':h.apellido})
                return Response({'Listado':prof_json})
            except ValueError:
                return Response({'Msj':"Valor erróneo"})
            except KeyError:
                return Response({'Msj':"Error de llave"})
        else:
            return Response({'Msj':"Error, método no soportado"})

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

@login_required()
def indexUpdateProfesional(request, idProfesional):
    user = request.user
    if user.is_authenticated:
        if Profesional.objects.filter(id=idProfesional).exists():
            profesional = Profesional.objects.get(id=idProfesional)
            return render(request, 'updateProfesional.html', {"profesional":profesional})
        else:
            messages.add_message(request=request, level = messages.ERROR, message='No existe el profesional')
            return redirect('home')
    else:
        return redirect('login2')


def addProfesional(request):
    user = request.user
    if user.is_authenticated:
        nombre = request.POST['Nombre']
        apellido = request.POST['Apellido']
        curp = request.POST['CURP']
        correo = request.POST['Correo']
        numero_1 = request.POST['Número 1']
        numero_2 = request.POST['Número 2']
        redes = request.POST['Redes']
        ubicacion = request.POST['Ubicación']
        especialidades = request.POST['Especialidades']
        servicios = request.POST['Servicios']
        valor = request.POST['Valor']
        redirectUrl = ''
        if nombre == '' or apellido == '' or curp == '':
            messages.add_message(request=request, level = messages.ERROR, message="No ha ingresado un campo requerido")
            redirectUrl = 'createTest'
        if correo != '' and es_correo_valido(correo) == False:
            messages.add_message(request=request, level = messages.ERROR, message="Ha ingresado un correo inválido")
            return render(request, 'updateProfesional.html', {"profesional" : profesional})
        else:
            try:
                profesional = Profesional.objects.create(
                    nombre = nombre,
                    apellido = apellido,
                    correo = correo,
                    numero_1 = numero_1,
                    numero_2 = numero_2,
                    redes = redes,
                    ubicacion = ubicacion,
                    especialidades = especialidades,
                    servicios = servicios,
                    valor = valor
                )
                messages.add_message(request=request, level = messages.SUCCESS, message="Profesional agregado correctamente")
                redirectUrl = 'home'
            except Exception as e:
                messages.add_message(request = request, level = messages.ERROR,message="Ha ocurrido un error al agregar al profesional")
                redirectUrl = 'createTest'
        return redirect(redirectUrl)
    else:
        return redirect('login2')

def updateProfesional(request, idProfesional):
    user = request.user
    if user.is_authenticated:
        nombre = request.POST['Nombre']
        apellido = request.POST['Apellido']
        curp = request.POST['CURP']
        correo = request.POST['Correo']
        numero_1 = request.POST['Número 1']
        numero_2 = request.POST['Número 2']
        redes = request.POST['Redes']
        ubicacion = request.POST['Ubicación']
        especialidades = request.POST['Especialidades']
        servicios = request.POST['Servicios']
        valor = request.POST['Valor']
        redirectUrl = ''
        profesional = Profesional.objects.get(id=idProfesional)
        if nombre == '' or apellido == '' or curp == '':
            messages.add_message(request=request, level = messages.ERROR, message="No ha ingresado un campo requerido")
            return render(request, 'updateProfesional.html', {"profesional" : profesional})
        if correo != '' and es_correo_valido(correo) == False:
            messages.add_message(request=request, level = messages.ERROR, message="Ha ingresado un correo inválido")
            return render(request, 'updateProfesional.html', {"profesional" : profesional})
        else:
            try:
                profesional.nombre = nombre,
                profesional.apellido = apellido,
                profesional.correo = correo,
                profesional.numero_1 = numero_1,
                profesional.numero_2 = numero_2,
                profesional.redes = redes,
                profesional.ubicacion = ubicacion,
                profesional.especialidades = especialidades,
                profesional.servicios = servicios,
                profesional.valor = valor
                profesional.save()
                messages.add_message(request=request, level = messages.SUCCESS, message="Profesional editado correctamente")
                redirectUrl = 'home'
            except Exception as e:
                messages.add_message(request=request, level = messages.ERROR, message="Ha ocurrido un error al editar al profesional")
                return render(request, 'updateProfesional.html',{"profesional":profesional})
            return redirect(redirectUrl)
    else:
        return redirect('login2')




