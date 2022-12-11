
import genericpath
from typing import Generic
from manualcrisis.models import models, Manual
from . import models
from users import models
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages


# cargar archivo PDF
def uploadManual(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if request.method == "POST":
                # Fetching the form data
                fileTitle = request.POST["fileTitle"]
                loadPDF = request.FILES["uploadPDF"]

                if Manual.objects.all().exists():
                    listfiles = Manual.objects.all()[:1].get()
                    listfiles.uploadPDF = loadPDF
                    listfiles.save()
                else:
                    # Saving the information in the database
                    termscondition = Manual.objects.create(
                        title=fileTitle,
                        uploadPDF=loadPDF
                    )
                return redirect('uploadManual')
            else:
                if Manual.objects.all().exists():
                    listfiles = Manual.objects.all()[:1].get()
                    return render(request, 'subirManual.html', context={
                        "files": listfiles.uploadPDF
                    })
                else:
                    listfiles = {}
                    return render(request, 'subirManual.html', context={"files": listfiles})
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
            getPDF = Manual.objects.get(pk=idtermsCondition)
            seePDF = {'PDF': getPDF.uploadPDF}

            return render(request, 'subirManual.html', {'Manual': getPDF, 'uploadPDF': getPDF.uploadPDF})
        else:
            messages.error(request, 'Do not have permission')
    else:
        return redirect('login2')
