from pickle import FALSE
from turtle import update
from unicodedata import name
from django.shortcuts import render, redirect
import profesional
from diario_emocional.models import Emocion
from diario_emocional.models import Entrada
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
import re
# Create your views here.

def get_All_Emocion(request, format=None):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            emocion = Emocion.objects.all()
            contexto = {'emocion': emocion}
            return render(request, 'administradorEmociones.html', contexto)
        else:
            messages.add_message(request=request, level=messages.SUCCESS, message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

@login_required()
def indexCreateEmocion(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'createEmocion.html')
    else:
        return redirect('login2')

def addEmocion(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            global emocion
            foto = request.FILES.get('Imagen')
            nombre = request.POST.get('Nombre')
            if isinstance(nombre, int):
                return Response({'Msj': 'Error, el nombre debe contener letras, no números'})
            redirectUrl = ''
            h_list_array = Emocion.objects.order_by('nombre')
            if foto == '' or nombre == '':
                messages.add_message(
                    request=request, level=messages.ERROR, message="No ha ingresado un nombre")
                return render(request, 'createEmocion.html')
            else:
                try:
                    emocion = Emocion.objects.create(
                        imagen_emocion=foto,
                        nombre=nombre
                    )
                    messages.add_message(
                        request=request, level=messages.SUCCESS, message="Emoción agregada correctamente")
                    redirect('pageadmin')
                except Exception as e:
                    messages.add_message(request=request, level=messages.ERROR,message="Ha ocurrido un error al agregar la emoción")
                    redirect('customer')
            return redirect('pageadmin')
        else:
            messages.add_message(request=request, level=messages.ERROR,message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('login2')
    else:
        return redirect('login2')

def updateEmocion(request, idEmocion):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            #foto = request.FILES['Imagen']
            nombre = request.POST['Nombre']
            if isinstance(nombre, int):
                return Response({'Msj': 'Error, el nombre debe contener letras, no números'})
            redirectUrl = ''
            emocion = Emocion.objects.get(id=idEmocion)
            if nombre == '':
                messages.add_message(
                    request=request, level=messages.SUCCESS, message="El Nombre es un campo requerido")
                return render(request, 'updateEmocion.html', {"emocion": emocion})
            else:
                try:
                    #emocion.imagen_profesional = foto
                    emocion.nombre = nombre
                    emocion.save()
                    messages.add_message(
                        request=request, level=messages.SUCCESS, message="Emoción editado correctamente")
                    return redirect('get_All_Emocion')
                except Exception as e:
                    messages.add_message(request=request, level=messages.SUCCESS,message="Ha ocurrido un error al editar la emoción")
                    return render(request, 'updateEmocion.html', {"emocion": emocion})
                return redirect(redirectUrl)
        else:
            messages.add_message(request=request, level=messages.SUCCESS,message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

@login_required()
def indexUpdateEmocion(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if Emocion.objects.filter().exists():
                firstProfesional = Emocion.objects.filter()[:1].get()
                emocion = Emocion.objects.get(id=firstProfesional.id)
                msg = "Emocion Configurada"
                emocion.save()
                return render(request, 'updateEmocion.html', {"emocion": emocion, "msgGood": msg})
            else:
                profesionalprimary = Emocion.objects.create(
                )
                messages.add_message(request=request, level=messages.SUCCESS,
                                     message="Por favor, vuelve a ingresar al area de 'profesional'")
                return redirect('pageadmin')
        else:
            messages.add_message(request=request, level=messages.SUCCESS,
                                 message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

def detalleEmocion(request, idEmocion):
    emocion = Emocion.objects.get(pk=idEmocion)
    return render(request, "detalleEmocion.html", {"emocion": emocion})

@login_required
def deleteEmocion(request, idEmocion):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if Emocion.objects.filter(id=idEmocion).exists():
                Emocion.objects.filter(pk=idEmocion).delete()
                messages.add_message(
                    request=request, level=messages.SUCCESS, message="Emoción eliminada correctamente")
                return redirect('pageadmin')
            else:
                messages.add_message(
                    request=request, level=messages.ERROR, message="No existe la emoción")
                return redirect('pageadmin')
        else:
            messages.add_message(request=request, level=messages.SUCCESS,message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

def editarEmocion(request, idEmocion):
    emocion = Emocion.objects.get(pk=idEmocion)
    return render(request, "updateEmocion.html", {"emocion": emocion})