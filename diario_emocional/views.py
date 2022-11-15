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

def valid_extension(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and
        not value.name.endswith('.gif') and
        not value.name.endswith('.bmp') and
            not value.name.endswith('.jpg')) and value.name is not None:
            return Response({'Msj': 'Error, formato no permitido'})

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
            if nombre == '':
                messages.add_message(
                    request=request, level=messages.ERROR, message="No ha ingresado un nombre")
                return render(request, 'createEmocion.html')
            if foto == None:
                messages.add_message( 
                    request=request, level=messages.ERROR, message="Error, debe subir foto para la emoción")
                return render(request, 'createEmocion.html')
            if valid_extension(foto):
                messages.add_message( 
                    request=request, level=messages.ERROR, message="Error, formato no permitido. Formatos permitidos: png, jpg, jpeg, gif, bmp")
                return render(request, 'createEmocion.html')
            else:
                try:
                    emocion = Emocion.objects.create(
                        imagen_emocion=foto,
                        nombre=nombre
                    )
                    messages.add_message(
                        request=request, level=messages.SUCCESS, message="Emoción agregada correctamente")
                    return redirect('/diario_emocional/allEmocion')
                except Exception as e:
                    messages.add_message(request=request, level=messages.ERROR,message="Ha ocurrido un error al agregar la emoción")
                    return redirect('/diario_emocional/allEmocion')
            return redirect('/emocion/allEmocion')
        else:
            messages.add_message(request=request, level=messages.ERROR,message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('login2')
    else:
        return redirect('login2')

def updateEmocion(request, idEmocion):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            foto = request.FILES['Imagen']
            nombre = request.POST['Nombre']
            if isinstance(nombre, int):
                return Response({'Msj': 'Error, el nombre debe contener letras, no números'})
            redirectUrl = ''
            emocion = Emocion.objects.get(id=idEmocion)
            if nombre == '':
                messages.add_message(
                    request=request, level=messages.SUCCESS, message="El Nombre es un campo requerido")
                return render(request, 'updateEmocion.html', {"emocion": emocion})
            if foto == None:
                messages.add_message( 
                    request=request, level=messages.ERROR, message="Error, debe subir foto para la emoción")
                return render(request, 'updateEmocion.html', {"emocion": emocion})
            if valid_extension(foto):
                messages.add_message( 
                    request=request, level=messages.ERROR, message="Error, formato no permitido. Formatos permitidos: png, jpg, jpeg, gif, bmp")
                return render(request, 'updateEmocion.html', {"emocion": emocion})
            else:
                try:
                    emocion.imagen_emocion = foto
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
                return redirect('/diario_emocional/allEmocion')
            else:
                messages.add_message(
                    request=request, level=messages.ERROR, message="No existe la emoción")
                return redirect('/diario_emocional/allEmocion')
        else:
            messages.add_message(request=request, level=messages.SUCCESS,message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')

def editarEmocion(request, idEmocion):
    emocion = Emocion.objects.get(pk=idEmocion)
    return render(request, "updateEmocion.html", {"emocion": emocion})

#Diario personal
@login_required 
def createDiario(request): 
    user = request.user 
    if user.is_authenticated: 
        return render(request, 'createDiario.html')
    else:
        return redirect('login2')
    
def createDiariosave(request):
    user = request.user
    if user.is_authenticated:
        tipo = Emocion.objects.get(pk = request.POST['Emocion'])
        emocion = request.POST.get('Emocion')
        descripcion = request.POST.get('Descripcion')
        if tipo == '' :
            messages.add_message(request, messages.INFO, 'Favor al menos ingrese su emoción, es importante para mantener un registro para ayudarlo más adelante')
            return redirect('createDiario')
        create_save = Entrada(
            emocion=tipo,
            descripcion=descripcion
            )
        create_save.save()
        messages.add_message(request, messages.INFO, 'Diario emocional registrado')
        return redirect('/diario_emocional/allDiario')
    else:
        return redirect('login2')

@login_required()
def indexUpdateDiario(request):
    user = request.user
    if user.is_authenticated:
        if Emocion.objects.filter().exists():
            firstEntrada = Entrada.objects.filter()[:1].get()
            diario = Emocion.objects.get(id=firstEntrada.id)
            msg = "Entrada de Diario Configurada"
            diario.save()
            return render(request, 'updateDiario.html', {"diario": diario, "msgGood": msg})
        else:
            entradaprimary = Emocion.objects.create(
            )
            messages.add_message(request=request, level=messages.SUCCESS,
                                    message="Por favor, vuelve a ingresar al area de 'diario'")
            return redirect('pageadmin')
    else:
        return redirect('login2')

@login_required
def updateDiariosave(request, idDiario): 
    user = request.user
    if user.is_authenticated:
        descripcion = request.POST.get (' Descripcion')
        emocion = request.POST.get('emocion')
        diario_data = Entrada.objects.get(id=idDiario)
        Entrada.objects.filter(pk=diario_data.id).update(descripcion=descripcion)                        
        Entrada.objects.filter(pk=diario_data.id).update(emocion=emocion)
        messages.add_message(request , messages.INFO , 'Diario actualizado con exito')
        return redirect ('diarioList')
    else:
        return redirect('login2')

def updateDiario(request, idEntrada):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            descripcion = request.POST.get('Descripcion')
            tipo = Emocion.objects.get(pk = request.POST['Emocion'])
            entrada = Entrada.objects.get(id=idEntrada)
            if tipo == '' :
                messages.add_message(request, messages.INFO, 'Favor al menos ingrese su emoción, es importante para mantener un registro para ayudarlo más adelante')
                return redirect('createDiario')
            else:
                try:
                    entrada.emocion = tipo
                    entrada.descripcion = descripcion
                    entrada.save()
                    messages.add_message(
                        request=request, level=messages.SUCCESS, message="Entrada de diario editada correctamente")
                    return redirect('/diario_emocional/allDiario')
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
        if Entrada.objects.filter(id=idEntrada).exists():
            Entrada.objects.filter(pk=idEntrada).delete()
            messages.add_message(
                request=request, level=messages.SUCCESS, message="Entrada de diario eliminada correctamente")
            return redirect('/diario_emocional/allDiario')
        else:
            messages.add_message(
                request=request, level=messages.ERROR, message="No existe la entrada de diario")
            return redirect('/diario_emocional/allDiario')
    else:
        return redirect('login2')


def viewDiario(request, format = None):
    user = request.user
    if user.is_authenticated:
        diario= Entrada.objects.all().count()
        diario_data= {'diario_data' : diario_data}
        return render(request , 'viewDiario.html' , diario_data )
    else:
        return redirect('login2') 

def get_All_Diario(request, format=None):
    user = request.user
    if user.is_authenticated:
        entrada = Entrada.objects.all()
        contexto = {'entrada': entrada}
        return render(request, 'listDiario.html', contexto)
    else:
        messages.add_message(request=request, level=messages.SUCCESS, message="No tiene suficientes permisos para ingresar a esta página")
        return redirect('login2')

def editarDiario(request, idEntrada):
    entrada = Entrada.objects.get(pk=idEntrada)
    return render(request, "updateDiario.html", {"entrada": entrada})

def detalleDiario(request, idEntrada):
    entrada = Entrada.objects.get(pk=idEntrada)
    return render(request, "detalleDiario.html", {"entrada": entrada})
