from django.shortcuts import render
from manualcrisis.models import Manual
from rest_framework.response import Response
from django.shortcuts import render, redirect
from pickle import FALSE
from turtle import update
from unicodedata import name
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
# Create your views here.


def valid_extension(value):
    if  (not value.name.endswith('.pdf') and
        not value.name.endswith('.docx') and
            value.name is not None):
            return Response({'Msj': 'Error, formato no permitido'})
        
        
@login_required()
def indexuploadManual ( request): 
    user = request.user
    if user.isauthenticated:
        if user.is_admin: 
            return render ( request, 'uploadManual.html')
        else : 
            return redirect('login2')
    else:
        return redirect('login2')

@login_required()
def uploadManual ( request) :
    user = request.user
    if user.isauthenticated:
        if user.is_admin: 
            manual = request.FILES.get ('Manual')
            title = request.POST('Titulo del manual')
            if title == '' : 
                messages.add_message(request=request, level=messages.ERROR, message="No ha ingresado un campo requerido")
                return render ( request , 'uploadManual.html')
            if valid_extension(manual): 
                messages.add_message(request=request, level=messages.ERROR, message="Error formato no permitido")
                return render ( request , 'uploadManual.html')
        else: 
            manual = Manual.objects.create(
                manual=manual,
                title=title
            )
            
            messages.add_message(request=request, level=messages.SUCCESS, message="Manual agregado correctamente")
            return redirect('/manualcrisis/allManual')
    else:
        return redirect('login2')    

@login_required()
def updateManual(request , idManual) : 
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            manual= request.FILES.get('Manual')
            title = request.POST.get('Titulo del manual')
            manual = Manual.objects.get(id=idManual)
        else:
            manual.manual=manual
            manual.title = title
            manual.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="Manual agregado correctamente")
            return redirect('/manualcrisis/allManual')
    else: 
        return redirect('login2')
    



@login_required()
def deleteManual(request, idManual): 
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if Manual.objects.filter(id=idManual).exists():
                Manual.objects.filter(pk=idManual).delete()
                messages.add_message(
                    request=request, level=messages.SUCCESS, message="Manual eliminado correctamente")
                return redirect('/manulcrisis/allManual')
            else:
                messages.add_message(
                    request=request, level=messages.ERROR, message="No existe el profesional")
                return redirect('/manualcrisis/allManual')
        else:
            messages.add_message(request=request, level=messages.SUCCESS,message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('customer')
    else:
        return redirect('login2')



def editarManuallist(request, idManual):
    manual = Manual.objects.get(pk=idManual)
    return render(request, "updateManual.html", {"manual": manual})



def deleteManuallist(request, idManual):
    manual = Manual.objects.get(pk=idManual)
    return render(request, "deleteManual.html", {"manual": manual})


