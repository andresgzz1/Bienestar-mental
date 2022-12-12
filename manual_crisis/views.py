from django.shortcuts import render

# Create your views here.

import genericpath
from typing import Generic

from rest_framework.response import Response
from manual_crisis.models import models, Manual
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
def subirManual(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if request.method == "POST":
                cargarPDF = request.FILES.get("subirPDF")
                if validar_extension(cargarPDF):
                    messages.add_message(request=request, level=messages.ERROR,
                                         message="Error, formato no permitido, debe subir archivos de tipo extension .PDF")
                    return redirect('subirManual')
                if Manual.objects.all().exists():
                    listarchivos = Manual.objects.all()[:1].get()
                    listarchivos.subirPDF = cargarPDF
                    listarchivos.save()
                else:
                    manualcrisis = Manual.objects.create(
                        subirPDF=cargarPDF
                    )
                    return redirect('subirManual')
            else:
                if Manual.objects.all().exists():
                    listarchivos = Manual.objects.all()[:1].get()
                    return render(request, 'subirManual.html', context={
                        "archivos": listarchivos.subirPDF, "archivos_get": listarchivos
                    })
                else:

                    listarchivos = Manual.objects.all()
                    return render(request, 'subirManual.html', context={"archivos": listarchivos, "archivos_get": listarchivos})
        else:
            messages.add_message(request=request, level=messages.SUCCESS,
                                 message="No tiene suficientes permisos para ingresar a esta página")
        return redirect('customer')

    else:
        return redirect('login2')


def mirarPDF(request, idManual):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            obtenerPDF = Manual.objects.get(pk=idManual)
            seePDF = {'PDF': obtenerPDF.subirPDF}

            return render(request, 'subirManual.html', {'manual': obtenerPDF, 'subirPDF': obtenerPDF.subirPDF})
        else:
            messages.error(request, 'Do not have permission')
    else:
        return redirect('login2')


def eliminarPDF(request, idManual):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if Manual.objects.filter(pk=idManual).exists():
                Manual.objects.filter(pk=idManual).delete()
                messages.add_message(
                    request=request, level=messages.SUCCESS, message="PDF borrado con éxito")
                return redirect('subirManual')
            else:
                messages.add_message(
                    request=request, level=messages.ERROR, message="No existe PDF")
                return redirect('subirManual')
        else:
            messages.add_message(request=request, level=messages.SUCCESS,
                                 message="No tiene suficientes permisos para ingresar a esta página")
            return redirect('login2')
    else:
        return redirect('login2')