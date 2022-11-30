
import genericpath
from typing import Generic
from config_web.models import models, termsCondition
from . import models
from users import models
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages


# cargar archivo PDF
def uploadFile(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if request.method == "POST":
                # Fetching the form data
                fileTitle = request.POST["fileTitle"]
                loadPDF = request.FILES["uploadPDF"]

                if termsCondition.objects.all().exists():
                    listfiles = termsCondition.objects.all()[:1].get()
                    listfiles.uploadPDF = loadPDF
                    listfiles.save()
                else:
                    # Saving the information in the database
                    termscondition = termsCondition.objects.create(
                        title=fileTitle,
                        uploadPDF=loadPDF
                    )
                return redirect('uploadFile')
            else:
                if termsCondition.objects.all().exists():
                    listfiles = termsCondition.objects.all()[:1].get()
                    return render(request, 'subirTerminos.html', context={
                        "files": listfiles.uploadPDF
                    })
                else:
                    listfiles = {}
                    return render(request, 'subirTerminos.html', context={"files": listfiles})
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
