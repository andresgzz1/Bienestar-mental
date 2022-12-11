
import genericpath
from typing import Generic

from rest_framework.response import Response
from config_web.models import models, termsCondition
from . import models
from users import models
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages


def validar_extension(value):
    if (not value.name.endswith('.pdf') and
        not value.name.endswith('.docx') and
            not value.name.endswith('.jpg')) and value.name is not None:
        return Response({'Msj': 'Error, formato no permitido'})


# cargar archivo PDF
def uploadFile(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if request.method == "POST":
                loadPDF = request.FILES["uploadPDF"]
                if validar_extension(loadPDF):
                    messages.add_message(request=request, level=messages.ERROR,
                                         message="Error, formato no permitido, debe subir archivos de tipo extension .PDF")
                    return redirect('uploadFile')
                if termsCondition.objects.all().exists():
                    listfiles = termsCondition.objects.all()[:1].get()
                    listfiles.uploadPDF = loadPDF
                    listfiles.save()
                else:
                    termscondition = termsCondition.objects.create(
                        uploadPDF=loadPDF
                    )
                    return redirect('uploadFile')
            else:
                if termsCondition.objects.all().exists():
                    listfiles = termsCondition.objects.all()[:1].get()
                    return render(request, 'subirTerminos.html', context={
                        "files": listfiles.uploadPDF, "files_get": listfiles
                    })
                else:

                    listfiles = termsCondition.objects.all()
                    return render(request, 'subirTerminos.html', context={"files": listfiles, "files_get": listfiles})
        else:
            messages.add_message(request=request, level=messages.SUCCESS,
                                 message="No tiene suficientes permisos para ingresar a esta página")
        return redirect('customer')

    else:
        return redirect('login2')


def verPDF(request, idtermsCondition):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            getPDF = termsCondition.objects.get(pk=idtermsCondition)
            seePDF = {'PDF': getPDF.uploadPDF}

            return render(request, 'subirTerminos.html', {'termsCondition': getPDF, 'uploadPDF': getPDF.uploadPDF})
        else:
            messages.error(request, 'Do not have permission')
    else:
        return redirect('login2')


def deletePDF(request, idtermsCondition):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if termsCondition.objects.filter(pk=idtermsCondition).exists():
                termsCondition.objects.filter(pk=idtermsCondition).delete()
                messages.add_message(
                    request=request, level=messages.SUCCESS, message="PDF deleted successfully")
                return redirect('uploadFile')
            else:
                messages.add_message(
                    request=request, level=messages.ERROR, message="DoesNotExist PDF")
                return redirect('uploadFile')
        else:
            messages.add_message(request=request, level=messages.SUCCESS,
                                 message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('login2')
    else:
        return redirect('login2')
