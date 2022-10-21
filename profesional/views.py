from pickle import FALSE
from unicodedata import name
from django.shortcuts import render,redirect,get_object_or_404
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
    expresion_regular = r"(?:(a-z0-9!#$%&'+/=?^_`{|}~-)+(?:\.(a-z0-9!#$%&'+/=?^_`{|}~-)+)|\"(?:(\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f)|\\(\x01-\x09\x0b\x0c\x0e-\x7f))\")@(?:(?:(a-z0-9)(?:(a-z0-9-)(a-z0-9))?\.)+(a-z0-9)(?:(a-z0-9-)(a-z0-9))?|\((?:(?:(2(5(0-5)|(0-4)(0-9))|1(0-9)(0-9)|(1-9)?(0-9)))\.){3}(?:(2(5(0-5)|(0-4)(0-9))|1(0-9)(0-9)|(1-9)?(0-9))|(a-z0-9-)*(a-z0-9):(?:(\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f)|\\(\x01-\x09\x0b\x0c\x0e-\x7f))+)\))"
    return re.match(expresion_regular, correo) is not None

#Templates Render
#Listar profesionales  
@login_required
def listProfesional(request,page =None, search=None):
    user = request.user
    if user.is_authenticated:
            
            if page == None:
                page = request.GET.get('page')
            else:
                page = page
            if request.GET.get('page') == None:
                    page = page
            else:
                    page = request.GET.get('page') 
            if search == None:
                    search = request.GET.get('search')
            else:
                    search = search
            if request.GET.get('search') == None:
                    search = search
            else:
                    search = request.GET.get('search') 
            if request.method == 'POST':
                    search = request.POST.get('search') 
                    page = None
            h_list = ()
            if search == None or search == "None":
                    h_count = Profesional.objects.all().count()
                    h_list_array = Profesional.objects.all()
                    for h in h_list_array:
                        h_list.append({'nombre':h.nombre,'apellido':h.apellido,'correo':h.correo,'numero_1':h.numero_1,'numero_2':h.numero_2,'redes':h.redes,'ubicacion':h.ubicacion ,'especialidades' : h.especialidades ,'servicios' : h.servicios , 'valor' : h.valor})
            else:
                    h_count = Profesional.objects.filter(nombre__icontains=search).count()
                    h_list_array = Profesional.objects.filter(nombre__icontains=search)
                    for h in h_list_array:
                        h_list.append({'nombre':h.nombre,'apellido':h.apellido,'correo':h.correo,'numero_1':h.numero_1,'numero_2':h.numero_2,'redes':h.redes,'ubicacion':h.ubicacion ,'especialidades' : h.especialidades ,'servicios' : h.servicios , 'valor' : h.valor})

            paginator = Paginator(h_list, 5) 
            h_list_paginate= paginator.get_page(page)   
            template_name = 'listProfesional.html'
            return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page})
        
    else:
        messages.add_message(request , messages.INFO , 'Favor ingrese a su cuenta')
        return redirect('login2')


    

@login_required()
def viewProfesional(request, idProfesional):
    user = request.user
    if user.is_authenticated:
            if Profesional.objects.filter(id=idProfesional).exists():
                Profesional.objects.get(id=idProfesional)
                return redirect('viewProfesional.html')
    else:
        return redirect('login2')



@login_required()
def createProfesional(request):
    user = request.user
    if user.is_admin:
        return render(request, 'createProfesional.html')
    else:
        messages.add_message(request=request, level = messages.ERROR, message="Ha ingresado a un area a la que no tiene permisos")
        return redirect('login2')
    
    
    
    
    
@login_required()
def createProfesionalsave(request):
    user = request.user
    if user.is_admin:
        imagen_profesional = request.FILES('imagen_profesional')
        nombre = request.POST('Nombre')
        if isinstance(nombre, int):
            return Response({'MSJ': 'Error, el nombre debe contener letras, no numeros.'})
        apellido = request.POST('Apellido')
        if isinstance(apellido, int):
            return Response({'MSJ': 'Error, el apellido debe contener letras, no numeros.'})
        curp = request.POST('CURP') 
        if curp == '':
            return Response({'Msj': "Favor ingrese CURP del profesional, este no puede quedar vacio."})
        correo = request.POST('Correo')
        if es_correo_valido(correo) == False:
            return Response({'MSJ': 'Error, el correo ingresado no es valido'})
        numero_1 = request.POST('Número 1')
        if isinstance(numero_1, str):
            return Response({'Msj':"El número ingresado es inválido. Por favor, reinténtelo."})
        
        numero_2 = request.POST('Número 2')
        if isinstance(numero_1, str):
            return Response({'Msj':"El número ingresado es inválido. Por favor, reinténtelo."})
        redes = request.POST('Redes')
        if redes == '':
            return Response({'Msj':"Favor complete las redes, en caso de no tener complete con NO EXISTE"})
        ubicacion = request.POST('Ubicación')
        if ubicacion == '':
            return Response({'Msj':"Ingrese la ubicación del profesional"})
        especialidades = request.POST('Especialidades')
        if especialidades == '':
            return Response({'Msj':"Favor ingrese la especialidad del profesional"})
        servicios = request.POST('Servicios')
        if servicios == '':
            return Response({'Msj':"Favor ingrese los servicios del profesional"})
        valor = request.POST('Valor')
        if valor == '':
            return Response({'Msj':"Favor ingrese los valores del profesional"})
        redirectUrl = 'createProfesional.html'
        try:
            create_save=Profesional(
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
            imagen_profesional =imagen_profesional,
            curp = curp,
            )
            create_save.save()
            messages.add_message(request=request, level = messages.SUCCESS, message="Profesional agregado correctamente")
            redirectUrl = 'listProfesional'
        except Exception as e:
                messages.add_message(request = request, level = messages.ERROR,message="Ha ocurrido un error al agregar al profesional")
                redirectUrl = 'createTest'
        return redirect(redirectUrl)
    else:
        messages.add_message(request=request, level = messages.SUCCESS, message="Intenta acceder sin permisos, favor ingrese como administrador")
        return redirect('login2')
    

@login_required()
def updateProfesional(request, idProfesional):
    user = request.user
    if user.is_admin:
        if Profesional.objects.filter(id=idProfesional).exists():
            profesional = Profesional.objects.get(id=idProfesional)
            return render(request, 'updateProfesional.html', {"profesional":profesional})
        else:
            messages.add_message(request=request, level = messages.ERROR, message='No existe el profesional')
            return redirect('home')
    else:
        return redirect('login2')


@login_required()
def updateProfesionalsave(request):
    user = request.user
    if user.is_admin:
            if request.method == 'POST':
                
                imagen_profesional = request.FILES.get('imagen_profesional')
                nombre = request.POST.get('Nombre')
                apellido = request.POST.get('Apellido')
                curp = request.POST.get('CURP')
                correo = request.POST.get('Correo')
                numero_1 = request.POST.get('Número 1')
                numero_2 = request.POST.get('Número 2')
                redes = request.POST.get('Redes')
                ubicacion = request.POST.get('Ubicación')
                especialidades = request.POST.get('Especialidades')
                servicios = request.POST.get('Servicios')
                valor = request.POST.get('Valor')
                profesional_data = Profesional.objects.get(idProfesional=curp)
                Profesional.objects.filter(id=profesional_data.id).update(nombre=nombre)                        
                Profesional.objects.filter(id=profesional_data.id).update(imagen_profesional=imagen_profesional)
                Profesional.objects.filter(id=profesional_data.id).update(apellido=apellido)
                Profesional.objects.filter(id=profesional_data.id).update(correo=correo)
                Profesional.objects.filter(id=profesional_data.id).update(numero_1=numero_1)
                Profesional.objects.filter(id=profesional_data.id).update(numero_2=numero_2)
                Profesional.objects.filter(id=profesional_data.id).update(ubicacion = ubicacion)
                Profesional.objects.filter(id=profesional_data.id).update(especialidades = especialidades)
                Profesional.objects.filter(id=profesional_data.id).update(servicios = servicios)
                Profesional.objects.filter(id=profesional_data.id).update(valor = valor)
                Profesional.objects.filter(id=profesional_data.id).update(redes = redes)
                messages.add_message(request , messages.INFO , 'Profesional actualizado con exito')
                return redirect ('listProfesional')
            else:
                messages.add_message(request, messages.INFO , 'Error en el método de envio')
                return redirect('listProfesional')
    else:
        messages.add_message(request , messages.INFO , 'Favor ingrese a su cuenta como administrador')
        return redirect('login2')


@login_required()
def deleteProfesional(request, idProfesional):
    user = request.user
    if user.is_admmin:
        if Profesional.objects.filter(id=idProfesional).exists():
            Profesional.objects.filter(id=idProfesional).delete()
            messages.add_message(request=request, level = messages.SUCCESS, message="Profesional eliminado correctamente")
            return redirect ('profesionalList')
        else:
            messages.add_message(request=request, level = messages.ERROR, message='No existe el profesional')
            return redirect('home')
    else:
        return redirect('login2')