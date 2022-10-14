from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from asyncio.windows_events import NULL

from email import message
from glob import glob
from http.client import ResponseNotReady
import profile
from re import template
import re
from sqlite3 import Time
from turtle import update
from webbrowser import get

# Create your views here.
import json
from ast import Return
from urllib import response
from models import Profesional
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None

# Create datos  
@api_view(['POST'])
def profesional_create(request, format=None):
        if request.method == 'POST':
            user = request.user
            if user.is_authenticated:
                if user.is_admin:
                    try:
                        imagen_profesional = request.FILES['imagen_profesional']
                        curp = request.data['curp']
                        if curp == '':
                            return Response({'Msj': "Favor ingrese CURP del profesional, este no puede quedar vacio."})
                        nombre = request.data['nombre']
                        if isinstance(nombre, int):
                            return Response({'MSJ': 'Error, el nombre debe contener letras, no numeros.'})
                        apellido = request.data['apellido']
                        if isinstance(apellido, int):
                            return Response({'MSJ': 'Error, el apellido debe contener letras, no numeros.'})
                        correo = request.data['correo']
                        if es_correo_valido(correo) == False:
                            return Response({'MSJ': 'Error, el correo ingresado no es valido'})
                        numero_1 = request.data['numero_1']
                        if isinstance(numero_1, str):
                            return Response({'Msj':"El número ingresado es inválido. Por favor, reinténtelo."})
                        numero_2 = request.data['numero_2']
                        if isinstance(numero_2,str):
                            return Response({'Msj':"El número ingresado es inválido. Por favor, reinténtelo."})
                        redes = request.data['redes']
                        ubicacion = request.data['ubicacion']
                        especialidades = request.data['especialidades']
                        if especialidades == '':
                            return Response({'Msj': "Favor ingrese especialidad(es) del profesional, esta no puede quedar vacio."})
                        servicios = request.data['servicios']
                        if servicios == '':
                            return Response({'Msj':"Favor ingrese un servicio del profesional."})
                        valor = request.data['valor']
                        if isinstance(valor, str):  
                            return Response({'Msj': "El valor debe ser un numero entero."})
                        if valor == '':
                            return Response({'Msj': 'Error, los valores no pueden estar vacios.'})
                        profesional_save = Profesional(
                            imagen_profesional = imagen_profesional,
                            curp = curp,
                            nombre = nombre,
                            apellido = apellido,
                            correo = correo,
                            numero_1 = numero_1,
                            numero_2 = numero_2,
                            redes = redes,
                            ubicacion = ubicacion,
                            especialidades = especialidades,
                            servicios = servicios,
                            valor = valor,
                        )
                        profesional_save.save()
                        Profesional.objects.filter(pk=id).update(estado="Ingresado")
                        return Response({'Msj': "Profesional agregado con exito"})
                    except Profesional.DoesExist:
                        return Response({'Msj':"Este profesional ya se encuentra en nuestra base de datos, favor rectifique los datos."})
                else:
                    return Response({'Msj':"No tienes suficientes permisos"})
        else:
            Response({'Msj': "Error método no soportado"})

#List Data
@api_view(['GET'])
def profesional_list(request, format=None):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            if user.is_admin:
                profesional_list = Profesional.objects.all()
                profesional_json = []
                for a in profesional_list:
                    profesional_json.append({
                    'imagen':a.imagen_profesional,
                    'curp':a.curp,
                    'nombre':a.nombre,
                    'apellido':a.apellido,
                    'correo':a.correo,
                    'numero_1':a.numero_1,
                    'numero_2':a.numero_2,
                    'redes':a.redes,
                    'ubicacion':a.ubicacion,
                    'especialidades':a.especialidades,
                    'servicios':a.servicios,
                    'valor':a.valor
                    })
                return Response({'List':profesional_json})
            else:
                return Response({'Msj':"No tienes suficientes permisos"})
    else:
        return Response({'Msj':"Error método no soportado"})

#Read por curp
@api_view(['POST'])
def read_profesional(request,format=None):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            if user.is_admin:
                try:
                    profesional_id = request.data['curp']
                    profesional_array_count = Profesional.objects.filter(profesional_id).count()
                    if  profesional_array_count>0:
                        profesional_array=Profesional.objects.filter(profesional_id)
                        profesional_json = []
                    for a in profesional_array:
                        profesional_json.append({
                        'imagen':a.imagen_profesional,
                        'curp':a.curp,
                        'nombre':a.nombre,
                        'apellido':a.apellido,
                        'correo':a.correo,
                        'numero_1':a.numero_1,
                        'numero_2':a.numero_2,
                        'redes':a.redes,
                        'ubicacion':a.ubicacion,
                        'especialidades':a.especialidades,
                        'servicios':a.servicios,
                        'valor':a.valor
                        })
                    return Response({'curp': profesional_json})
                except Profesional.DoesNotExist:
                    return Response ({'MSJ': 'Error no hay coincidencias'})
                except ValueError:
                    return Response ({'MSJ': 'Valor no soportado'})
            else:
                return Response({'Msj':"No tienes suficientes permisos"})
    else:
        return Response({'Msj': "Error método no soportado"})

# Update data
@api_view(['POST'])
def update_profesional(request, format=None):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            if user.is_admin:
                try:  
                    curp = request.data['curp']  
                    if curp == '':
                        return Response({'Msj': "Favor ingrese CURP del profesional, este no puede quedar vacio."})
                    imagen_profesional = request.FILES['imagen_profesional']
                    nombre = request.data['nombre']
                    if isinstance(nombre, int):
                        return Response({'MSJ': 'Error, el nombre debe contener letras, no numeros.'})
                    apellido = request.data['apellido']
                    if isinstance(apellido, int):
                        return Response({'MSJ': 'Error, el apellido debe contener letras, no numeros.'})
                    correo = request.data['correo']
                    if es_correo_valido(correo) == False:
                        return Response({'MSJ': 'Error, el correo ingresado no es valido'})
                    numero_1 = request.data['numero_1']
                    if isinstance(numero_1, str):
                        return Response({'Msj':"El número ingresado es inválido. Por favor, reinténtelo."})
                    numero_2 = request.data['numero_2']
                    if isinstance(numero_2,str):
                        return Response({'Msj':"El número ingresado es inválido. Por favor, reinténtelo."})
                    redes = request.data['redes']
                    ubicacion = request.data['ubicacion']
                    especialidades = request.data['especialidades']
                    if especialidades == '':
                        return Response({'Msj': "Favor ingrese especialidad(es) del profesional, esta no puede quedar vacio."})
                    servicios = request.data['servicios']
                    if servicios == '':
                        return Response({'Msj':"Favor ingrese un servicio del profesional."})
                    valor = request.data['valor']
                    if isinstance(valor, str):  
                        return Response({'Msj': "El valor debe ser un numero entero."})
                    if valor == '':
                        return Response({'Msj': 'Error, los valores no pueden estar vacios.'})
                    if imagen_profesional != NULL and nombre != '' and apellido != '' and correo != '' and (numero_1 != '' or numero_2 != '') and redes != '' and ubicacion != '' and especialidades != '' and servicios != '' and valor != '':
                        Profesional.objects.filter(pk=curp).update(imagen_profesional=imagen_profesional)
                        Profesional.objects.filter(pk=curp).update(nombre=nombre)
                        Profesional.objects.filter(pk=curp).update(apellido=apellido)
                        Profesional.objects.filter(pk=curp).update(correo=correo)
                        Profesional.objects.filter(pk=curp).update(numero_1=numero_1)
                        Profesional.objects.filter(pk=curp).update(numero_2=numero_2)
                        Profesional.objects.filter(pk=curp).update(redes=redes)
                        Profesional.objects.filter(pk=curp).update(ubicacion=ubicacion)
                        Profesional.objects.filter(pk=curp).update(especialidades=especialidades)
                        Profesional.objects.filter(pk=curp).update(servicios=servicios)
                        Profesional.objects.filter(pk=curp).update(valor=valor)
                        profesional_json=[]
                        profesional_array = Profesional.objects.get(pk=curp)
                        profesional_json.append({
                        'imagen':profesional_array.imagen_profesional,
                        'curp':profesional_array.curp,
                        'nombre':profesional_array.nombre,
                        'apellido':profesional_array.apellido,
                        'correo':profesional_array.correo,
                        'numero_1':profesional_array.numero_1,
                        'numero_2':profesional_array.numero_2,
                        'redes':profesional_array.redes,
                        'ubicacion':profesional_array.ubicacion,
                        'especialidades':profesional_array.especialidades,
                        'servicios':profesional_array.servicios,
                        'valor':profesional_array.valor
                        })
                        return Response({'Msj': "Update realizado con exito" , profesional_array.nombre:profesional_json})
                except Profesional.DoesNotExist:
                    return Response({'Msj':"Error no hay coincidencias"})
            else:
                return Response({'Msj':"No tienes suficientes permisos"})
    else:
        return Response({'Msj': 'Error método no soportado'})

# Delete data
@api_view(['POST'])
def delete_profesional(request, format=None):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            if user.is_admin:
                try:
                    curp = request.data['curp']
                    profesional_array = Profesional.objects.get(pk=curp)
                    curp = profesional_array.curp
                    if profesional_array:
                        Profesional.objects.filter(pk=curp).delete()
                        return Response({'Msj': 'Profesional eliminado con éxito'})
                except Profesional.DoesNotExist:
                    return Response({'Msj' : "Error no se encuentra el profesional registrado"})
                except ValueError:
                    return Response({'Msj':"Favor ingrese un número valido de CURP"})
            else:
                return Response({'Msj':"No tienes suficientes permisos"})
    else:
        return Response({'Msj': 'Error método no soportado'})  
        

###templates 


