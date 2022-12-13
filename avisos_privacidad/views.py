import genericpath
from typing import Generic

from rest_framework.response import Response
from avisos_privacidad.models import models, avisosPrivacidad
from . import models
from users import models
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages


def valida_extension(value):
    if (not value.name.endswith('.pdf') and
        not value.name.endswith('.docx') and
            not value.name.endswith('.pdf')) and value.name is not None:
        return Response({'Msj': 'Error, formato no permitido'})


# cargar archivo PDF
def cargarArchivo(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if request.method == "POST":
                loadPDF = request.FILES["cargarArchivo"]
                if valida_extension(loadPDF):
                    messages.add_message(request=request, level=messages.ERROR,
                                         message="Error, formato no permitido, debe subir archivos de tipo extension .PDF")
                    return redirect('cargarArchivo')
                if avisosPrivacidad.objects.all().exists():
                    listfiles = avisosPrivacidad.objects.all()[:1].get()
                    listfiles.uploadPDF = loadPDF
                    listfiles.save()
                else:
                    avisosprivacidad = avisosPrivacidad.objects.create(
                        uploadPDF=loadPDF
                    )
                    return redirect('cargarArchivo')
            else:
                if avisosPrivacidad.objects.all().exists():
                    listfiles = avisosPrivacidad.objects.all()[:1].get()
                    return render(request, 'subirPrivacidad.html', context={
                        "files": listfiles.uploadPDF, "files_get": listfiles
                    })
                else:

                    listfiles = avisosPrivacidad.objects.all()
                    return render(request, 'subirPrivacidad.html', context={"files": listfiles, "files_get": listfiles})
        else:
            messages.add_message(request=request, level=messages.SUCCESS,
                                 message="No tiene suficientes permisos para ingresar a esta página")
        return redirect('customer')

    else:
        return redirect('login2')


def verAvisos(request, idavisosPrivacidad):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            getPDF = avisosPrivacidad.objects.get(pk=idavisosPrivacidad)
            seePDF = {'PDF': getPDF.uploadPDF}

            return render(request, 'subirPrivacidad.html', {'avisosPrivacidad': getPDF, 'uploadPDF': getPDF.uploadPDF})
        else:
            messages.error(request, 'Do not have permission')
    else:
        return redirect('login2')


def deleteAvisos(request, idavisosPrivacidad):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if avisosPrivacidad.objects.filter(pk=idavisosPrivacidad).exists():
                avisosPrivacidad.objects.filter(pk=idavisosPrivacidad).delete()
                messages.add_message(
                    request=request, level=messages.SUCCESS, message="PDF deleted successfully")
                return redirect('cargarArchivo')
            else:
                messages.add_message(
                    request=request, level=messages.ERROR, message="DoesNotExist PDF")
                return redirect('cargarArchivo')
        else:
            messages.add_message(request=request, level=messages.SUCCESS,
                                 message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('login2')
    else:
        return redirect('login2')
