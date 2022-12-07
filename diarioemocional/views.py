from pickle import FALSE
from turtle import update
from unicodedata import name
from django.shortcuts import render, redirect
import profesional
from diarioemocional.models import Entrada
from users.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
import re

# Create your views here.

def valid_extension(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and
        not value.name.endswith('.gif') and
        not value.name.endswith('.bmp') and
            not value.name.endswith('.jpg')) and value.name is not None:
            return Response({'Msj': 'Error, formato no permitido'})

#Diario personal
@login_required 
def createDiario(request): 
    user = request.user 
    if user.is_authenticated:
        if user.is_client:
            return render(request, 'createDiario.html')
        else:
            return redirect('login2')
    else:
            return redirect('login2')
    
def createDiariosave(request):
    user = request.user
    if user.is_authenticated:
        if user.is_client:
            emocion = request.POST.get('Emocion')
            descripcion = request.POST.get('Descripcion')
            if emocion == '' :
                messages.add_message(request, messages.INFO, 'Favor al menos ingrese su emoción, es importante para mantener un registro para ayudarlo más adelante')
                return redirect('createDiario')
            create_save = Entrada(
                user = request.user,
                emocion=emocion,
                descripcion=descripcion
                )
            create_save.save()
            messages.add_message(request, messages.INFO, 'Diario emocional registrado')
            return redirect('/diarioemocional/allDiario')
        else:
            return redirect('login2')
    else:
            return redirect('login2')

@login_required
def updateDiariosave(request, idDiario): 
    user = request.user
    if user.is_authenticated:
        if user.is_client:
            descripcion = request.POST.get (' Descripcion')
            emocion = request.POST.get('Emocion')
            diario_data = Entrada.objects.get(id=idDiario)
            Entrada.objects.filter(pk=diario_data.id).update(descripcion=descripcion)                        
            Entrada.objects.filter(pk=diario_data.id).update(emocion=emocion)
            messages.add_message(request , messages.INFO , 'Diario actualizado con exito')
            return redirect ('diarioList')
        else:
            return redirect('login2')
    else:
            return redirect('login2')

def updateDiario(request, idEntrada):
    user = request.user
    if user.is_authenticated:
        if user.is_client:
            descripcion = request.POST.get('Descripcion')
            emocion = request.POST.get('Emocion')
            entrada = Entrada.objects.get(id=idEntrada)
            if emocion == '' :
                messages.add_message(request, messages.INFO, 'Favor al menos ingrese su emoción, es importante para mantener un registro para ayudarlo más adelante')
                return redirect('createDiario')
            else:
                try:
                    entrada.emocion = emocion
                    entrada.descripcion = descripcion
                    entrada.save()
                    messages.add_message(
                        request=request, level=messages.SUCCESS, message="Entrada de diario editada correctamente")
                    return redirect('/diarioemocional/allDiario')
                except Exception as e:
                    messages.add_message(request=request, level=messages.SUCCESS,message="Ha ocurrido un error al editar la emoción")
                    return render(request, 'updateDiario.html')
                return redirect(redirectUrl)
        else:
            messages.add_message(request=request, level=messages.SUCCESS,message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')
    
    
@login_required
def deleteDiario(request, idEntrada):
    user = request.user
    if user.is_authenticated:
        if user.is_client:
            if Entrada.objects.filter(id=idEntrada).exists():
                Entrada.objects.filter(pk=idEntrada).delete()
                messages.add_message(
                    request=request, level=messages.SUCCESS, message="Entrada de diario eliminada correctamente")
                return redirect('/diarioemocional/allDiario')
            else:
                messages.add_message(
                    request=request, level=messages.ERROR, message="No existe la entrada de diario")
                return redirect('/diarioemocional/allDiario')
        else:
            return redirect('login2')
    else:
        return redirect('login2')


def viewDiario(request, format = None):
    user = request.user
    if user.is_authenticated:
        if user.is_client:
            diario= Entrada.objects.all().count()
            diario_data= {'diario_data' : diario_data}
            return render(request , 'viewDiario.html' , diario_data )
        else:
            return redirect('login2') 
    else:
        return redirect('login2')

def get_All_Diario(request, format=None):
    user = request.user
    if user.is_authenticated:
        if user.is_client:
            entrada = Entrada.objects.filter(user_id=user)
            contexto = {'entrada': entrada}
            return render(request, 'listDiario.html', contexto)
        else:
            messages.add_message(request=request, level=messages.SUCCESS, message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('login2')
    else:
        return redirect('login2')

def editarDiario(request, idEntrada):
    entrada = Entrada.objects.get(pk=idEntrada)
    return render(request, "updateDiario.html", {"entrada": entrada})

def detalleDiario(request, idEntrada):
    entrada = Entrada.objects.get(pk=idEntrada)
    return render(request, "detalleDiario.html", {"entrada": entrada})
