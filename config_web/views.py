from django.contrib.auth import authenticate, login, logout
from testdass.models import testregister1

from . import models
from users import models
from django.shortcuts import render, redirect
from urllib import response
from users.models import User, userStandard
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from django.http import HttpResponse


def uploadFile(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            filetitle = request.POST('title')
            uploadFile = request.FILES('uploadedFile')

            termsCondition = models.termsCondition(
                title=filetitle,
                uploadFile=uploadFile

            )
            termsCondition.save()
            termsCondition = models.termsCondition.objects.all()
            return render(request, 'config_web/upload-file.html', {'uploadFile': uploadFile})
        else:
            messages.add_message(
                request=request, level=messages.ERROR, message="Do not Have permissions")
        return('customer')
    else:
        return('login2')
