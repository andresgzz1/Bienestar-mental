
from config_web.models import models, termsCondition
from . import models
from users import models
from django.shortcuts import render, redirect
from django.contrib import messages


def uploadFile(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            if request.method == "POST":
                # Fetching the form data
                fileTitle = request.POST["fileTitle"]
                loadPDF = request.FILES["uploadPDF"]

                # Saving the information in the database
                termscondition = termsCondition.objects.create(
                title=fileTitle,
                uploadPDF=loadPDF
                )
                termscondition.save()
                print(loadPDF)

            else:
                listfiles = termsCondition.objects.all()[:1].get()
                return render(request, 'upload-file.html', context={
                    "files": listfiles
                })

        else:
            messages.add_message(request=request, level=messages.SUCCESS,
                                    message="No tiene suficientes permisos para ingresar a esta página")
        return redirect('uploadFile')

    else:
        return redirect('login2')

    
