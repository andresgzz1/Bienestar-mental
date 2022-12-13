from urllib.parse import urlencode
from django.shortcuts import render

# Create your views here.from cgitb import text
from genericpath import exists
from unicodedata import name
from django.shortcuts import render, redirect
from avisos_privacidad.models import avisosPrivacidad
from config_web.models import termsCondition
from manual_crisis.models import Manual

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import requests

from testdass.models import alternative1, link_techniques1, question1, recomendation1, relaxation_techniques1, respuestas_user1, test1, testregister1, thermometer_config
from users.models import User, userStandard
# Create your views here.

#Endpoint 
@api_view(['GET'])
def get_All_Test(request, format=None):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            try:
                forms_list= test1.objects.all()
                forms_json=[]
                for h in forms_list:
                    forms_json.append({'name': h.name, 'rut': h.description})
                return Response({'Listado': forms_json })
            except ValueError:
                return Response({'Msj': "Valor erroneo"})
            except KeyError:
                return Response({'Msj': "Error de llave"})
    else:
        return Response({'Msj': "Error metodo no soportado"})
        
#Templates Render


@login_required()
def indexViewTest(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            return render(request, 'admin/createTest.html')
        else:
            return redirect('login2')
    else:
        return redirect('login2')


@login_required()
def indexCreateTest(request):
    user = request.user
    if user.is_authenticated and user.is_admin:
        return render(request, 'admin/createTest.html')
    else:
        return redirect('login2')


@login_required()
def indexUpdateTest(request):
    user = request.user
    if termsCondition.objects.all().exists():
        loadfile = termsCondition.objects.all()[:1].get()
    else:
        loadfile = None
    if Manual.objects.all().exists():
        loadmanual = Manual.objects.all()[:1].get()
    else:
        loadmanual = None
    if avisosPrivacidad.objects.all().exists():
        loadavisos = avisosPrivacidad.objects.all()[:1].get()
    else:
                loadavisos = None
    if user.is_authenticated and user.is_admin:
        try:
            if test1.objects.filter().exists():
                firstTest = test1.objects.filter()[:1].get()
                test = test1.objects.get(id=firstTest.id)
                questions = question1.objects.filter(test_id = test.id)

                contadorDepre = 0
                contadorAnsi = 0
                contadorEstr = 0
                depresionText = 'depresion'
                ansiedadText = 'ansiedad'
                estresTexto = 'estres'
                normalText = 'normal'

                """ obtener colores """
                color_1 = ""
                color_2 = ""
                color_3 = ""
                color_4 = ""
                color_5 = ""
                if not thermometer_config.objects.filter().exists():
                    therConfig = thermometer_config.objects.create()
                    color_1 = therConfig.color_1
                    color_2 = therConfig.color_2
                    color_3 = therConfig.color_3
                    color_4 = therConfig.color_4
                    color_5 = therConfig.color_5
                else:
                    therConfig = thermometer_config.objects.filter()[:1].get()
                    color_1 = therConfig.color_1
                    color_2 = therConfig.color_2
                    color_3 = therConfig.color_3
                    color_4 = therConfig.color_4
                    color_5 = therConfig.color_5



                for quest in questions:
                    if quest.question_type == "depresion":
                        contadorDepre = contadorDepre + 1
                    elif quest.question_type == "ansiedad":
                        contadorAnsi = contadorAnsi + 1
                    elif quest.question_type == "estres":
                        contadorEstr = contadorEstr + 1

                
                
                if contadorDepre !=7 or contadorAnsi !=7 or contadorEstr != 7:
                    msg = "Test desconfigurado"
                    if test.state_config == True:
                        test.state_config = False
                        test.save()
                    return render(request, 'admin/updateTest.html', {"test" : test, "questions": questions, "msg":msg, 'depresionText':depresionText,'ansiedadText': ansiedadText , 'normalText': normalText, 'estresTexto': estresTexto, 'color_1': color_1, 'color_2': color_2, 'color_3': color_3, 'color_4':color_4, 'color_5': color_5, 'loadfile': loadfile, 'loadavisos':loadavisos, 'loadmanual':loadmanual
} )
                else:
                    msg = "Test Configurado"
                    if test.state_config == False:
                        test.state_config = True
                        test.save()
                    return render(request, 'admin/updateTest.html', {"test" : test, "questions": questions, "msgGood":msg, 'depresionText':depresionText ,'ansiedadText': ansiedadText , 'normalText': normalText, 'estresTexto': estresTexto, 'color_1': color_1, 'color_2': color_2, 'color_3': color_3, 'color_4':color_4, 'color_5': color_5,'loadfile': loadfile, 'loadavisos':loadavisos, 'loadmanual':loadmanual
} )
    
                return render(request, 'admin/updateTest.html', context)
            else:
                """ Inicializar test """
                testprimary = test1.objects.create()
                """ Inicializar color tabla termometro """
                colorConfig = thermometer_config.objects.create()

                messages.add_message(request=request, level = messages.SUCCESS, message="Porfavor, vuelve a ingresar al area de 'test'")
                return redirect('pageadmin')

        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Error al responder Test")
            return redirect('pageadmin')


    else:
        return redirect('login2')

@login_required()
def indexCreateQuestion(request):
    user = request.user
    if user.is_authenticated and user.is_admin:
        return render(request, 'admin/createQuestion.html')
    else:
        return redirect('login2')


@login_required()
def viewQuestion(request, idQuestion):
    user = request.user
    if user.is_authenticated and user.is_admin:
            question = question1.objects.get(id=idQuestion)
            alternatives = alternative1.objects.filter(question_id = question.id)
            return render(request, 'admin/viewQuestion.html', {"question": question, "alternatives": alternatives} )

    else:
        return redirect('login2')
        
@login_required()
def viewAutoDiagnostic(request):
    user = request.user
    if user.is_authenticated and (user.is_client or user.is_admin):
        try:

                firstTest = test1.objects.filter()[:1].get()
                if test1.objects.filter(id=firstTest.id).exists():   
                    if firstTest.state_config == True:
                        
                        """ Eliminar registros del usuario que se encuentren en estado 0 """
                        if testregister1.objects.filter(status=0).filter(user_id=user.id).exists():
                            testregister1.objects.filter(status=0).filter(user_id=user.id).delete()

                        """ Crear registro de usuario """
                        testRegister = testregister1.objects.create(
                            user_id = user.id,
                            test_id = firstTest.id,
                            status = 0
                        )
                        return redirect('viewResp_test', testRegister.id)

                    else:
                        messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos el test no está disponible, vuelva pronto.")
                        return redirect('customer')
                else:
                    messages.add_message(request=request, level = messages.SUCCESS, message="No Existe el Test")
                    return redirect('customer')

        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, en éste momento no está disponible el Test")
            return redirect('customer')
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')


@login_required()
def viewRecomendation(request, disorder, level, testregister_id):
    user = request.user
    if termsCondition.objects.all().exists():
        loadfile = termsCondition.objects.all()[:1].get()
    else:
        loadfile = None
    if Manual.objects.all().exists():
        loadmanual = Manual.objects.all()[:1].get()
    else:
        loadmanual = None
    if avisosPrivacidad.objects.all().exists():
        loadavisos = avisosPrivacidad.objects.all()[:1].get()
    else:
        loadavisos = None
    if user.is_authenticated and (user.is_admin or user.is_client):
        try:
            if testregister1.objects.filter(id=testregister_id).exists():
                testRegister = testregister1.objects.get(id=testregister_id)
                recomendation = recomendation1.objects.filter(level=disorder)[:1].get()
                techniques = relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).filter(level=level)[:1].get()
                links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)
                return render(request, 'user/viewRecomendation.html', {'recomendation':recomendation, 'techniques': techniques, 'links': links, 'testRegister': testRegister, 'loadfile': loadfile, 'loadavisos':loadavisos, 'loadmanual':loadmanual
})
            else:
                messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, en éste momento no está disponible la recomendación")
                return redirect('customer')
        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, en éste momento no está disponible la recomendación")
            return redirect('customer' )
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')




@login_required()
def viewRecomendationAll(request,page=None,search=None, filterType=None, filterOrden=None):
    user = request.user
    if termsCondition.objects.all().exists():
        loadfile = termsCondition.objects.all()[:1].get()
    else:
        loadfile = None
    if Manual.objects.all().exists():
        loadmanual = Manual.objects.all()[:1].get()
    else:
        loadmanual = None
    if avisosPrivacidad.objects.all().exists():
        loadavisos = avisosPrivacidad.objects.all()[:1].get()
    else:
        loadavisos = None
    if user.is_authenticated:
        try:
            h_list = []
            
            """ Page """
            if page == None:
                page = request.GET.get('page')
            else:
                page = page
            if request.GET.get('page') == None:
                page = page
            else:
                page = request.GET.get('page') 
            """ Search """    
            if search == None:
                search = request.GET.get('search')
            else:
                search = search
            if request.GET.get('search') == None:
                search = search
            else:
                search = request.GET.get('search') 
            if request.method == 'POST':
                search = request.POST.get('search') 
                page = None
            if (search == None or search == "None") and filterType == None:
                if filterOrden=='default':
                    h_list_array = link_techniques1.objects.all().order_by('id')
                elif filterOrden=='date':
                    h_list_array = link_techniques1.objects.all().order_by('created_at')
                elif filterOrden=='name':
                    h_list_array = link_techniques1.objects.all().order_by('text_title')
                elif filterOrden=='origen':
                    h_list_array = link_techniques1.objects.all().order_by('origen')
                elif filterOrden=='canal':
                    h_list_array = link_techniques1.objects.all().order_by('canal')
                elif filterOrden=='autor':
                    h_list_array = link_techniques1.objects.all().order_by('autor')
                for h in h_list_array:
                    h_list.append(h)
            elif(search == None or search == "None") and filterType == 'all':
                if filterOrden=='default':
                    h_list_array = link_techniques1.objects.all().order_by('id')
                elif filterOrden=='date':
                    h_list_array = link_techniques1.objects.all().order_by('created_at')
                elif filterOrden=='name':
                    h_list_array = link_techniques1.objects.all().order_by('text_title')
                elif filterOrden=='origen':
                    h_list_array = link_techniques1.objects.all().order_by('origen')
                elif filterOrden=='canal':
                    h_list_array = link_techniques1.objects.all().order_by('canal')
                elif filterOrden=='autor':
                    h_list_array = link_techniques1.objects.all().order_by('autor')
                for h in h_list_array:
                    h_list.append(h)
            elif(search == None or search == "None") and filterType == 'depresion':
                recomendation = recomendation1.objects.get(level='depresion')
                niveles = relaxation_techniques1.objects.filter(recomendation_id=recomendation.id)
                for n in niveles:

                    if filterOrden=='default':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('id')
                    elif filterOrden=='date':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('created_at')

                    elif filterOrden=='name':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('text_title')

                    elif filterOrden=='origen':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('origen')

                    elif filterOrden=='canal':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('canal')

                    elif filterOrden=='autor':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('autor')

        
                    for h in h_list_array:
                        h_list.append(h) 
            elif(search == None or search == "None") and filterType == 'ansiedad':
                recomendation = recomendation1.objects.get(level='ansiedad')
                niveles = relaxation_techniques1.objects.filter(recomendation_id=recomendation.id)
                for n in niveles:

                    if filterOrden=='default':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('id')
                    elif filterOrden=='date':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('created_at')

                    elif filterOrden=='name':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('text_title')

                    elif filterOrden=='origen':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('origen')

                    elif filterOrden=='canal':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('canal')

                    elif filterOrden=='autor':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('autor')


                    for h in h_list_array:
                        h_list.append(h) 

            elif(search == None or search == "None") and filterType == 'estres':
                recomendation = recomendation1.objects.get(level='estres')
                niveles = relaxation_techniques1.objects.filter(recomendation_id=recomendation.id)
                for n in niveles:

                    if filterOrden=='default':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('id')
                    elif filterOrden=='date':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('created_at')

                    elif filterOrden=='name':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('text_title')

                    elif filterOrden=='origen':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('origen')

                    elif filterOrden=='canal':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('canal')

                    elif filterOrden=='autor':
                        h_list_array = link_techniques1.objects.all().filter(relaxation_techniques_id = n.id).order_by('autor')


                    for h in h_list_array:
                        h_list.append(h) 
            else:
                if filterType == 'depresion':
                    recomendation = recomendation1.objects.get(level='depresion')
                    niveles = relaxation_techniques1.objects.filter(recomendation_id=recomendation.id)
                    for n in niveles:
                        if filterOrden=='default':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('created_at')
                        elif filterOrden=='date':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('created_at')
                        elif filterOrden=='name':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('text_title')
                        elif filterOrden=='origen':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('origen')
                        elif filterOrden=='canal':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('canal')
                        elif filterOrden=='autor':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('autor')

                        for h in h_list_array:
                            h_list.append(h) 
                if filterType == 'ansiedad':
                    recomendation = recomendation1.objects.get(level='ansiedad')
                    niveles = relaxation_techniques1.objects.filter(recomendation_id=recomendation.id)
                    for n in niveles:


                        if filterOrden=='default':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('id')
                        elif filterOrden=='date':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('created_at')
                        elif filterOrden=='name':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('text_title')
                        elif filterOrden=='origen':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('origen')
                        elif filterOrden=='canal':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('canal')
                        elif filterOrden=='autor':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('autor')

                        for h in h_list_array:
                            h_list.append(h) 

                if filterType == 'estres':
                    recomendation = recomendation1.objects.get(level='estres')
                    niveles = relaxation_techniques1.objects.filter(recomendation_id=recomendation.id)
                    for n in niveles:

                        
                        if filterOrden=='default':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('id')
                        elif filterOrden=='date':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('created_at')
                        elif filterOrden=='name':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('text_title')
                        elif filterOrden=='origen':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('origen')
                        elif filterOrden=='canal':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('canal')
                        elif filterOrden=='autor':
                            h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).filter(relaxation_techniques_id = n.id).order_by('autor')

                        for h in h_list_array:
                            h_list.append(h) 
                elif filterType == 'all':

                    if filterOrden=='default':
                        h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).order_by('id')
                    elif filterOrden=='date':
                        h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).order_by('created_at')
                    elif filterOrden=='name':
                        h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).order_by('text_title')
                    elif filterOrden=='origen':
                        h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).order_by('origen')
                    elif filterOrden=='canal':
                        h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).order_by('canal')
                    elif filterOrden=='autor':
                        h_list_array = link_techniques1.objects.all().filter(text_title__icontains=search).order_by('autor')

                    for h in h_list_array:
                        h_list.append(h) 

            paginator = Paginator(h_list, 6) 
            h_list_paginate= paginator.get_page(page)  

            links = link_techniques1.objects.all()
            return render(request, 'user/viewRecomendation_all.html', {'links': links,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search, 'filterType': filterType, 'filterOrden': filterOrden, 'loadfile': loadfile, 'loadavisos':loadavisos, 'loadmanual':loadmanual
})
        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, en éste momento no está disponible la recomendación")
            return redirect('customer' )
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')


@login_required()
def viewRecomendationFilter(request):
    user = request.user
    if user.is_authenticated:        
        filterType = request.POST.get('optionType')
        filterOrden = request.POST.get('filterOrden')
        filterTypeValue = ""
        filterTypeValue2 = ""
        """ Type """
        if filterType == None:
            filterTypeValue = "all"
        if filterType == 'all':
            filterTypeValue = "all"
        if filterType == 'depresion':
            filterTypeValue = "depresion"
        if filterType == 'ansiedad':
            filterTypeValue = "ansiedad"
        if filterType == 'estres':
            filterTypeValue = "estres"
        """ Orden """
        if filterOrden == None:
            filterTypeValue2 = "default"
        if filterOrden == 'default':
            filterTypeValue2 = "default"
        if filterOrden == 'date':
            filterTypeValue2 = "date"
        if filterOrden == 'name':
            filterTypeValue2 = "name"
        if filterOrden == 'origen':
            filterTypeValue2 = "origen"
        if filterOrden == 'canal':
            filterTypeValue2 = "canal"
        if filterOrden == 'autor':
            filterTypeValue2 = "autor"

        return redirect('viewRecomendationAll',filterTypeValue,filterTypeValue2)

    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')

@login_required()
def viewRecomendationAdmin(request, disorder, level, returnPage, page=None):
    user = request.user
    if termsCondition.objects.all().exists():
        loadfile = termsCondition.objects.all()[:1].get()
    else:
        loadfile = None
    if Manual.objects.all().exists():
        loadmanual = Manual.objects.all()[:1].get()
    else:
        loadmanual = None
    if avisosPrivacidad.objects.all().exists():
        loadavisos = avisosPrivacidad.objects.all()[:1].get()
    else:
        loadavisos = None
    if user.is_authenticated and user.is_admin:
            """ Page """
            if page == None:
                page = request.GET.get('page')
            else:
                page = page
            if request.GET.get('page') == None:
                page = page
            else:
                page = request.GET.get('page') 

            #Inicializar recomendations and techniques
            if not recomendation1.objects.all().exists():
                inicializarTablas(request)
                recomendation = recomendation1.objects.filter(level=disorder)[:1].get()
                techniques = relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).filter(level=level)[:1].get()
                links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)

                paginator = Paginator(links, 3) 
                h_list_paginate= paginator.get_page(page)  

                return render(request, 'user/viewRecomendation.html', {'recomendation':recomendation, 'techniques': techniques, 'links': h_list_paginate, 'paginator':paginator,'page':page})
            else:
                recomendation = recomendation1.objects.filter(level=disorder)[:1].get()
                techniques = relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).filter(level=level)[:1].get()
                links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)

                paginator = Paginator(links, 3) 
                h_list_paginate = paginator.get_page(page) 


                return render(request, 'admin/viewRecomendationAdmin.html', {'recomendation':recomendation, 'techniques': techniques,'links': h_list_paginate, 'returnPage': returnPage, 'paginator':paginator,'page':page,'loadfile': loadfile, 'loadavisos':loadavisos, 'loadmanual':loadmanual
})

    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')


@login_required()
def indexIntroTest(request):
    user = request.user
    if termsCondition.objects.all().exists():
        loadfile = termsCondition.objects.all()[:1].get()
    else:
        loadfile = None
    if Manual.objects.all().exists():
        loadmanual = Manual.objects.all()[:1].get()
    else:
        loadmanual = None
    if avisosPrivacidad.objects.all().exists():
        loadavisos = avisosPrivacidad.objects.all()[:1].get()
    else:
        loadavisos = None
    if user.is_authenticated:
        if test1.objects.filter().exists():
            firstTest = test1.objects.filter()[:1].get()
            if firstTest.state_config == 1:
                return render(request, 'user/intro_autodiagnostic.html', {'test': firstTest,'loadfile': loadfile, 'loadavisos':loadavisos, 'loadmanual':loadmanual
})
            else:
                messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos el test no está disponible, vuelva pronto.")
                return redirect('customer')
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos el test no está disponible, vuelva pronto.")
            return redirect('customer')

    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')






@login_required()
def indexViewResult(request, testregister_id):
    user = request.user
    if termsCondition.objects.all().exists():
        loadfile = termsCondition.objects.all()[:1].get()
    else:
        loadfile = None
    if Manual.objects.all().exists():
        loadmanual = Manual.objects.all()[:1].get()
    else:
        loadmanual = None
    if avisosPrivacidad.objects.all().exists():
        loadavisos = avisosPrivacidad.objects.all()[:1].get()
    else:
        loadavisos = None
    if user.is_authenticated:
        depresionText = 'depresion'
        ansiedadText = 'ansiedad'
        estresText = 'estres'
        stateDepre = False
        stateAnsi = False
        stateEstres = False
        stateProfesionalDepre = False
        stateProfesionalAnsi = False
        testRegist = testregister1.objects.get(id=testregister_id)
        color_1 = ""
        color_2 = ""
        color_3 = ""
        color_4 = ""
        color_5 = ""
        if not thermometer_config.objects.filter().exists():
            therConfig = thermometer_config.objects.create()
            color_1 = therConfig.color_1
            color_2 = therConfig.color_2
            color_3 = therConfig.color_3
            color_4 = therConfig.color_4
            color_5 = therConfig.color_5
        else:
            therConfig = thermometer_config.objects.filter()[:1].get()
            color_1 = therConfig.color_1
            color_2 = therConfig.color_2
            color_3 = therConfig.color_3
            color_4 = therConfig.color_4
            color_5 = therConfig.color_5


        userStand = userStandard.objects.get(user_id = user.id)
        userSelect = {'id': user.id, 'image': user.imagen_profesional.url,'username': user.username, 'is_client': user.is_client, 'is_admin': user.is_admin, 'first_name': user.first_name,
                        'last_name': user.last_name, 'email': user.email, 'matricula': userStand.matricula, 'created_at': user.date_joined, 'phone': userStand.phone, 'sexo': userStand.sexo, 'ubicacion': userStand.ubication, 'fecha_nacimiento': userStand.birth_date}

        #Validar Recomendacion Depresión
        if recomendation1.objects.filter(level = 'depresion').exists():
            recomendation = recomendation1.objects.filter(level = 'depresion')[:1].get()

            if relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).exists():
                relax_tech = relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).filter(level = testRegist.result_depresion)[:1].get()
                stateProfesionalDepre = relax_tech.state_professional
                if link_techniques1.objects.filter(relaxation_techniques_id = relax_tech.id).exists():
                    stateDepre = True
        
        #Validar Recomendación Ansiedad
        if recomendation1.objects.filter(level = 'ansiedad').exists():
            recomendation = recomendation1.objects.filter(level = 'ansiedad')[:1].get()

            if relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).exists():
                relax_tech = relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).filter(level = testRegist.result_ansiedad)[:1].get()
                stateProfesionalAnsi = relax_tech.state_professional
                if link_techniques1.objects.filter(relaxation_techniques_id = relax_tech.id).exists():
                    stateAnsi = True
        
        #Validar Recomendación Estres
        if recomendation1.objects.filter(level = 'estres').exists():
            recomendation = recomendation1.objects.filter(level = 'estres')[:1].get()

            if relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).exists():
                relax_tech = relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).filter(level = testRegist.result_estres)[:1].get()
                if link_techniques1.objects.filter(relaxation_techniques_id = relax_tech.id).exists():
                    stateEstres = True
        

        return render(request, 'user/termometro.html', {'testRegist': testRegist,'depresionText':depresionText, 'ansiedadText':ansiedadText,'estresText':estresText, 'stateDepre': stateDepre, 'stateAnsi': stateAnsi, 'stateEstres': stateEstres,'stateProfesionalDepre': stateProfesionalDepre, 'stateProfesionalAnsi': stateProfesionalAnsi, 'userSelect':userSelect, 'color_1': color_1, 'color_2': color_2, 'color_3': color_3, 'color_4': color_4, 'color_5': color_5,'loadfile': loadfile, 'loadavisos':loadavisos, 'loadmanual':loadmanual
})
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')

        

#Pendiente evaluar validaciones
def addTest(request):
    user = request.user
    if user.is_authenticated and user.is_admin:

        nombre = request.POST['txtNombre']
        pretest_text = request.POST['txtPretest']
        redirectUrl = ''

        if nombre == '':
            messages.add_message(request=request, level = messages.SUCCESS, message="El Nombre es un campo requerido")
            redirectUrl = 'createTest'

        else:
            try:
                test = test1.objects.create(
                name = nombre,
                pretest_text = pretest_text
                )
                messages.add_message(request=request, level = messages.SUCCESS, message="Test agregado correctamente")
                redirectUrl = 'home'
                
            except Exception as e:
                messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al agregar el Test")
                redirectUrl = 'createTest'
        return redirect(redirectUrl)
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')





def updateTest(request, idTest):
    user = request.user
    if user.is_authenticated and user.is_admin:

        nombre = request.POST['txtNombre']
        pretest = request.POST['txtPretest']
        introduction = request.POST['txtIntroduction']

        redirectUrl = ''
        test = test1.objects.get(id=idTest)



        if nombre == '':
            messages.add_message(request=request, level = messages.SUCCESS, message="El Nombre es un campo requerido")
            return render(request, 'admin/updateTest.html', {"test" : test} )

        else:
            try:
                test.name = nombre
                test.pretest_text = pretest
                test.introduction_text = introduction
                test.save()
                messages.add_message(request=request, level = messages.SUCCESS, message="Test editado correctamente")
                return redirect('updateTest')
                
            except Exception as e:
                messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al editar el Test")
                return render(request, 'admin/updateTest.html', {"test" : test} )

            return redirect(redirectUrl)
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')




#Agregar pregunta a test
def addCuestion(request):
    user = request.user
    if user.is_authenticated and user.is_admin:

        firstTest = test1.objects.filter()[:1].get()
        questionsTotal = question1.objects.filter(test_id = firstTest.id)
        question = request.POST['txtQuestion']
        type = request.POST['txtType']
        redirectUrl = ''

        if question == '':
            messages.add_message(request=request, level = messages.SUCCESS, message="La Pregunta es un campo requerido")
            redirectUrl = 'createQuestion'
        

        else:
            try:
                    questions = question1.objects.filter(question_type = type)
                    if questions.count() == 7:
                        messages.add_message(request=request, level = messages.SUCCESS, message="Error: Las preguntas de "+type+" ya han sido configuradas, no puedes agregar más.")
                        return redirect('updateTest')
                    elif questions.count() == 6:
                        questionAdd = question1.objects.create(
                        test = firstTest,
                        question_text = question,
                        question_type = type
                        )

                        for x in range(1,5):
                            alternative = alternative1.objects.create(
                                question = questionAdd,
                                alternative = x
                            )
                        messages.add_message(request=request, level = messages.SUCCESS, message="Pregunta Agregada correctamente. Haz configurado las preguntas de tipo "+type+" correctamente.")
                        return redirect('updateTest')
                    else:
                        questionAdd = question1.objects.create(
                        test = firstTest,
                        question_text = question,
                        question_type = type
                        )

                        for x in range(1,5):
                            alternative = alternative1.objects.create(
                                question = questionAdd,
                                alternative = x
                            )
                        messages.add_message(request=request, level = messages.SUCCESS, message="Pregunta agregada correctamente")
                        return redirect('updateTest')
                
                
            except Exception as e:
                messages.add_message(request=request, level = messages.SUCCESS, message= e)
                return redirect('updateTest')
        return redirect(redirectUrl)
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')

#Guardar pregunta en primer test
def saveQuestion(request, idQuestion):
    user = request.user
    if user.is_authenticated and user.is_admin:

        firstTest = test1.objects.filter()[:1].get()
        question = request.POST['txtQuestion']
        type = request.POST['txtType']


        if question == '':
            messages.add_message(request=request, level = messages.SUCCESS, message="La Pregunta es un campo requerido")
            return redirect('updateTest')

        else:
            try:
                questionSave = question1.objects.get(id=idQuestion)

                questionsTotal = question1.objects.filter(test_id = firstTest.id)

                questions = question1.objects.filter(question_type = type)
                if questions.count() == 7:
                    if questionSave.question_type != type:
                        msg_error = "No puedes agregar más preguntas de la categoría "+ type+"."
                        return render(request, 'admin/updateTest.html', {"test" : firstTest, "questions": questionsTotal, "msg":msg_error} )
                    else:

                        questionSave.question_text = question
                        questionSave.question_type = type
                        questionSave.save()

                        messages.add_message(request=request, level = messages.SUCCESS, message="Pregunta guardada correctamente")
                        return redirect('updateTest')

                elif questions.count() == 6:
                    questionSave.question_text = question
                    questionSave.question_type = type
                    questionSave.save()

                    messages.add_message(request=request, level = messages.SUCCESS, message="Pregunta guardada correctamente")
                    return redirect('updateTest')
                else:
                    questionSave.question_text = question
                    questionSave.question_type = type
                    questionSave.save()

                    messages.add_message(request=request, level = messages.SUCCESS, message="Pregunta guardada correctamente")
                    return redirect('updateTest')

                
            except Exception as e:
                messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al guardar la pregunta")
                return redirect('updateTest')
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')


#Agregar pregunta a test
def deleteQuestion(request, idQuestion):
    user = request.user
    if user.is_authenticated and user.is_admin:
        firstTest = test1.objects.filter()[:1].get()
        try:
            questionDelete = question1.objects.get(id=idQuestion)
            questionDelete.delete()

            messages.add_message(request=request, level = messages.SUCCESS, message="Pregunta eliminada correctamente")
            return redirect('updateTest')
            
        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al eliminar la pregunta")
            return redirect('updateTest')
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')

#Agregar pregunta a test
def saveColor(request):
    user = request.user
    if user.is_authenticated and user.is_admin:
        firstTest = test1.objects.filter()[:1].get()
        try:
            color_1 = request.POST['txtColor1']
            color_2 = request.POST['txtColor2']
            color_3 = request.POST['txtColor3']
            color_4 = request.POST['txtColor4']
            color_5 = request.POST['txtColor5']

            configcolor = thermometer_config.objects.filter()[:1].get()
            configcolor.color_1 = color_1
            configcolor.color_2 = color_2
            configcolor.color_3 = color_3
            configcolor.color_4 = color_4
            configcolor.color_5 = color_5
            configcolor.save()

            messages.add_message(request=request, level = messages.SUCCESS, message="Colores del termómetro guardados correctamente")
            return redirect('updateTest')
            
        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="No se han podido guardar los colores del termómetro")
            return redirect('updateTest')
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')

#Guardar pregunta en primer test
def saveResp(request, testRegisterId, questionId):
    user = request.user

    if user.is_authenticated:
        try:
            alternative = request.POST['flexRadioDefault']
            if alternative == '4':
                messages.add_message(request=request, level = messages.SUCCESS, message="Por favor seleccione una alternativa.")
                return redirect('viewResp_test', testRegisterId)
            else:
                if testregister1.objects.filter(id=testRegisterId).exists() or question1.objects.filter(id=questionId).exists:
                    registerSelected = testregister1.objects.get(id=testRegisterId)
                    questionSelect = question1.objects.get(id=questionId)

                    testRegister = respuestas_user1.objects.create(
                        alternative = alternative,
                        testregister = registerSelected,
                        question_id = questionId,
                        question_text = questionSelect.question_text,
                        question_type = questionSelect.question_type
                    ) 

                    return redirect('viewResp_test', testRegisterId)
                else:
                    messages.add_message(request=request, level=messages.SUCCESS, message="Ha ocurrido un problema, lo sentimos.")
                    return redirect('customer')

        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, ha ocurrido un error al cargar la página, vuerva a intentar porfavor...")
            redirect('customer')
   
   
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')


#REgistrar test
def registerTest(request, testregister_id):
    user = request.user
    if user.is_authenticated:
        try:
            registerSelected = testregister1.objects.get(id=testregister_id)
            firstTest = test1.objects.filter()[:1].get()
            questions = question1.objects.filter(test_id = firstTest.id)
            respuestasUser = respuestas_user1.objects.filter(testregister_id=testregister_id)


            """ Deben haber 7 preguntas de cada tipo """
            contadorDepre = 0
            contadorAnsiedad = 0
            contadorEstres = 0
            sumDepre = 0
            sumAnsi = 0
            sumEst = 0

            for resp in respuestasUser:
                if resp.question_type == 'depresion':
                    contadorDepre = contadorDepre + 1
                    sumDepre = sumDepre + resp.alternative
                elif resp.question_type == 'ansiedad':
                    contadorAnsiedad = contadorAnsiedad + 1
                    sumAnsi = sumAnsi + resp.alternative
                elif resp.question_type == 'estres':
                    contadorEstres = contadorEstres + 1
                    sumEst = sumEst + resp.alternative


            if contadorDepre == 7 and contadorAnsiedad==7 and contadorEstres==7:
                
                sumDepre = sumDepre*2
                sumAnsi = sumAnsi*2
                sumEst = sumEst*2

                #Depresión resultado
                resultDepre = ""
                if 0 <= sumDepre <= 9:
                    resultDepre = "normal"
                if 10 <= sumDepre <= 13:
                    resultDepre = "mild"
                if 14 <= sumDepre <= 20:
                    resultDepre = "moderate"
                if 21 <= sumDepre <= 27:
                    resultDepre = "severe"
                if 28 <= sumDepre:
                    resultDepre = "Extremely Severe"
                
                #Anxiety result
                resultAnx = ""
                if 0 <= sumAnsi <= 7:
                    resultAnx = "normal"
                if 8 <= sumAnsi <= 9:
                    resultAnx = "mild"
                if 10 <= sumAnsi <= 14:
                    resultAnx = "moderate"
                if 15 <= sumAnsi <= 19:
                    resultAnx = "severe"
                if 20 <= sumAnsi:
                    resultAnx = "Extremely Severe"
                
                #Stress result
                resultStress = ""
                if 0 <= sumEst <= 14:
                    resultStress = "normal"
                if 15 <= sumEst <= 18:
                    resultStress = "mild"
                if 19 <= sumEst <= 25:
                    resultStress = "moderate"
                if 26 <= sumEst <= 33:
                    resultStress = "severe"
                if 34 <= sumEst:
                    resultStress = "Extremely Severe"
                
                sumaTotal = sumDepre + sumAnsi + sumEst

                registerSelected.status=1
                registerSelected.result_depresion = resultDepre
                registerSelected.result_ansiedad = resultAnx
                registerSelected.result_estres = resultStress
                registerSelected.result_total = sumaTotal
                registerSelected.save()
                return redirect('indexViewResult',testregister_id=registerSelected.id)
            else:
                messages.add_message(request=request, level = messages.SUCCESS, message="Porfavor, responda todas las preguntas.")
                return redirect('customer')
            
        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al responder el test")
            return redirect('customer')
    else:
        return redirect('login2')





""" TEST """

@login_required()
def viewResp_test(request, testreg_id):
    user = request.user
    if termsCondition.objects.all().exists():
        loadfile = termsCondition.objects.all()[:1].get()
    else:
        loadfile = None
    if Manual.objects.all().exists():
        loadmanual = Manual.objects.all()[:1].get()
    else:
        loadmanual = None
    if avisosPrivacidad.objects.all().exists():
        loadavisos = avisosPrivacidad.objects.all()[:1].get()
    else:
        loadavisos = None
    if user.is_authenticated:
        try:
            firstTest = test1.objects.filter()[:1].get()
            if firstTest.state_config == True:
                questionsForm = question1.objects.filter(test_id=firstTest.id)
                questionRes = respuestas_user1.objects.filter(testregister_id=testreg_id)
                
                questions_ok = []
                questions_form = []
                # iteración de las preguntas del formulario y preguntas respondidas por el usuario
                for qForm in questionsForm:
                    questions_form.append(qForm.id)
                    for qRes in questionRes:
                        if qForm.id == qRes.question_id:
                            questions_ok.append(qRes.question_id)
                        

                b = list(set(questions_form) - set(questions_ok))
                # get count of total questions in form and questions answered
                count_total_question = len(questions_form) 
                count_question = (count_total_question- len(b)) + 1


                if b == []:

                    return redirect('registerTest', testreg_id)
                else:
                    numero = b[:1]
                    numero_value = numero[0]
                    question = question1.objects.get(id = numero_value)

                    return render(request, 'user/resp_test.html', {"test" : firstTest, "question": question, "testregister": testreg_id, 'count_question': count_question, 'count_question_total': count_total_question,'loadfile': loadfile, 'loadavisos':loadavisos, 'loadmanual':loadmanual
} )
            else:
                messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos el test no está disponible, vuelva pronto.")
                return redirect('customer')

        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, en éste momento no está disponible el Test")
            return redirect('customer')
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')





""" Función filtrar liks según niveles de depresion/ansiedad """
@login_required()
def funFilterLinks(request, disorder, level):

    user = request.user
    if user.is_authenticated:
        try:
            filterLevel = request.GET.get('selectLevel2')
            recomendation = recomendation1.objects.filter(level=disorder)[:1].get()
            if relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).filter(level=filterLevel).exists():
                techniques = relaxation_techniques1.objects.filter(recomendation_id = recomendation.id).filter(level=filterLevel)[:1].get()
                links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)
            else:
                messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, el nivel ingresado aún no se registra")
                techniques = relaxation_techniques1.objects.filter(recomendation_id = recomendation.id)[:1].get()
                links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)
            return redirect('viewRecomendationAdmin', recomendation.level, techniques.level, 'True')
        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, en éste momento no está disponible la recomendación")
            return redirect('pageadmin')
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')


""" agregar liks de recomendaciones """
@login_required()
def addLinkRecomendation(request, id_relaxation_tech):

    user = request.user
    if user.is_authenticated and user.is_admin:
        try:
            titulo = request.POST['txtTitulo']
            url = request.POST['txtUrl']
            autor = request.POST['txtAutor']
            canal = request.POST['txtCanal']
            origen = request.POST['txtOrigen']
            
            checker_url_yt = "https://www.youtube.com/oembed?url="
            checker_url_vm = "https://vimeo.com/api/oembed.json?url="

            video_url_yt = checker_url_yt + url
            video_url_vm = checker_url_vm + url

            techniques = relaxation_techniques1.objects.get(id=id_relaxation_tech)
            recomendation = recomendation1.objects.get(id=techniques.recomendation_id)
            links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)    
        
            try:
                requestURLyt = requests.get(video_url_yt)
                requestURLvm = requests.get(video_url_vm)

                if requestURLyt.status_code == 200 or requestURLvm.status_code == 200:

                    link = link_techniques1.objects.create(
                        text_title = titulo,
                        url = url,
                        autor = autor,
                        canal = canal,
                        origen = origen,
                        relaxation_techniques = techniques
                    )

                    messages.add_message(request=request, level = messages.SUCCESS, message="Link Agregado correctamente")
                    return redirect('viewRecomendationAdmin', recomendation.level, techniques.level, 'True')

                else:
                    messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, el link ingresado no está disponible en YouTube o Vimeo")
                    return redirect('viewRecomendationAdmin', recomendation.level, techniques.level, 'True')
            except Exception as e:
                    messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, ha ocurrido un error")
                    return redirect('viewRecomendationAdmin', recomendation.level, techniques.level, 'True')

        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, en éste momento no está disponible la recomendación")
            return redirect('pageadmin')
    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')



""" eliminar liks de recomendaciones """
@login_required()
def deleteLinkRecomendation(request, id_relaxation_tech, id_link):

    user = request.user
    if user.is_authenticated and user.is_admin:
        
        linkDelate = link_techniques1.objects.filter(id= id_link).delete()
        
        techniques = relaxation_techniques1.objects.get(id=id_relaxation_tech)
        recomendation = recomendation1.objects.get(id=techniques.recomendation_id)
        links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)

        messages.add_message(request=request, level = messages.SUCCESS, message="Link eliminado correctamente")
        return redirect('viewRecomendationAdmin', recomendation.level, techniques.level, 'True')

    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')

""" editar liks de recomendaciones """
@login_required()
def editLinkRecomendation(request, id_relaxation_tech, id_link):

    user = request.user
    if user.is_authenticated and user.is_admin:
        
        titulo = request.POST['txtTitulo']
        url = request.POST['txtUrl']
        autor = request.POST['txtAutor']
        canal = request.POST['txtCanal']
        origen = request.POST['txtOrigen']
        
        checker_url_yt = "https://www.youtube.com/oembed?url="
        checker_url_vm = "https://vimeo.com/api/oembed.json?url="

        video_url_yt = checker_url_yt + url
        video_url_vm = checker_url_vm + url

        techniques = relaxation_techniques1.objects.get(id=id_relaxation_tech)
        recomendation = recomendation1.objects.get(id=techniques.recomendation_id)
        links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)    
    
        try:
            requestURLyt = requests.get(video_url_yt)
            requestURLvm = requests.get(video_url_vm)

            if requestURLyt.status_code == 200 or requestURLvm.status_code == 200:

                recomendation = link_techniques1.objects.get(id=id_link)

                recomendation.text_title = titulo
                recomendation.url = url
                recomendation.autor = autor
                recomendation.canal = canal
                recomendation1.origen = origen

                recomendation.save()
                
                techniques = relaxation_techniques1.objects.get(id=id_relaxation_tech)
                recomendation = recomendation1.objects.get(id=techniques.recomendation_id)
                links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)

                messages.add_message(request=request, level = messages.SUCCESS, message="Link editado correctamente")
                return redirect('viewRecomendationAdmin', recomendation.level, techniques.level, 'True')

            else:
                messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, el link ingresado no está disponible en YouTube o Vimeo")
                return redirect('viewRecomendationAdmin', recomendation.level, techniques.level, 'True')
        except Exception as e:
                messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, ha ocurrido un error.")
                return redirect('viewRecomendationAdmin', recomendation.level, techniques.level, 'True')

    else:   
        messages.add_message(request=request, level = messages.ERROR, message="No tienes los permisos suficientes, lo sentimos.")
        return redirect('login2')



""" agregar liks de recomendaciones """
@login_required()
def saveTechniques(request, id_relaxation_tech):

    user = request.user
    if user.is_authenticated and user.is_admin:
        try:
            profesional = request.POST.get('use_profesional', '') == 'on'
            mensaje = request.POST['txtTextMsg']

            tech = relaxation_techniques1.objects.get(id=id_relaxation_tech)
            tech.text_msg = mensaje
            tech.state_professional = profesional
            tech.save()
            
            techniques = relaxation_techniques1.objects.get(id=id_relaxation_tech)
            recomendation = recomendation1.objects.get(id=techniques.recomendation_id)
            links = link_techniques1.objects.filter(relaxation_techniques_id = techniques.id)


            messages.add_message(request=request, level = messages.SUCCESS, message="Cambios guardados correctamente")
            return redirect('viewRecomendationAdmin', recomendation.level, techniques.level, 'True')
        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Lo sentimos, en éste momento no está disponible la recomendación")
            return redirect('pageadmin')
    else: 
        return redirect('login2')






""" Funciones """

def inicializarTablas(request):
    depre = recomendation1.objects.create(
            text_msg = 'Texto depresion',
            level = 'depresion'
            )
    ansiedad = recomendation1.objects.create(
            text_msg = 'Texto ansiedad',
            level = 'ansiedad'
        )
    estres = recomendation1.objects.create(
            text_msg = 'Texto estres',
            level = 'estres'
        )
    #Depresion
    relaxation_techniques1.objects.create(
            recomendation = depre,
            text_msg = '',
            level='normal'
        )
    relaxation_techniques1.objects.create(
            recomendation = depre,
            text_msg = '',
            level='mild'
        )
    relaxation_techniques1.objects.create(
            recomendation = depre,
            text_msg = '',
            level='moderate'
        )
    relaxation_techniques1.objects.create(
            recomendation = depre,
            text_msg = '',
            level='severe'
        )
    relaxation_techniques1.objects.create(
            recomendation = depre,
            text_msg = '',
            level='Extremely Severe'
        )
    #Ansiedad
    relaxation_techniques1.objects.create(
            recomendation = ansiedad,
            text_msg = '',
            level='normal'
        )
    relaxation_techniques1.objects.create(
            recomendation = ansiedad,
            text_msg = '',
            level='mild'
        )
    relaxation_techniques1.objects.create(
            recomendation = ansiedad,
            text_msg = '',
            level='moderate'
        )
    relaxation_techniques1.objects.create(
            recomendation = ansiedad,
            text_msg = '',
            level='severe'
        )
    relaxation_techniques1.objects.create(
            recomendation = ansiedad,
            text_msg = '',
            level='Extremely Severe'
        )
    #Estres
    relaxation_techniques1.objects.create(
            recomendation = estres,
            text_msg = '',
            level='normal'
        )
    relaxation_techniques1.objects.create(
            recomendation = estres,
            text_msg = '',
            level='mild'
        )
    relaxation_techniques1.objects.create(
            recomendation = estres,
            text_msg = '',
            level='moderate'
        )
    relaxation_techniques1.objects.create(
            recomendation = estres,
            text_msg = '',
            level='severe'
        )
    relaxation_techniques1.objects.create(
            recomendation = estres,
            text_msg = '',
            level='Extremely Severe'
        )
    
    return True
