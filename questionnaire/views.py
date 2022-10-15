from unicodedata import name
from django.shortcuts import render, redirect
from questionnaire.models import Alternative, Question, Test
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

#Endpoint 
@api_view(['GET'])
def get_All_Test(request, format=None):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            try:
                forms_list= Test.objects.all()
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
            return render(request, 'createTest.html')
        else:
            return redirect('login2')
    else:
        return redirect('login2')


@login_required()
def indexCreateTest(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'createTest.html')
    else:
        return redirect('login2')


@login_required()
def indexUpdateTest(request, idTest):
    user = request.user
    if user.is_authenticated:

        if Test.objects.filter(id=idTest).exists():
            test = Test.objects.get(id=idTest)
            questions = Question.objects.filter(test_id = test.id)

            return render(request, 'updateTest.html', {"test" : test, "questions": questions} )
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="No Existe el Test")
            return redirect('home')

    else:
        return redirect('login2')

@login_required()
def viewQuestion(request, idQuestion):
    user = request.user
    if user.is_authenticated:
            question = Question.objects.get(id=idQuestion)
            alternatives = Alternative.objects.filter(question_id = question.id)
            return render(request, 'viewQuestion.html', {"question": question, "alternatives": alternatives} )

    else:
        return redirect('login2')
        

#Pendiente evaluar validaciones
def addTest(request):
    user = request.user
    if user.is_authenticated:

        nombre = request.POST['txtNombre']
        descripcion = request.POST['txtDescripcion']
        redirectUrl = ''

        if nombre == '':
            messages.add_message(request=request, level = messages.SUCCESS, message="El Nombre es un campo requerido")
            redirectUrl = 'createTest'

        else:
            try:
                test = Test.objects.create(
                name = nombre,
                description = descripcion
                )
                messages.add_message(request=request, level = messages.SUCCESS, message="Test agregado correctamente")
                redirectUrl = 'home'
                
            except Exception as e:
                messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al agregar el Test")
                redirectUrl = 'createTest'
        return redirect(redirectUrl)
    else:
        return redirect('login2')




def updateTest(request, idTest):
    user = request.user
    if user.is_authenticated:

        nombre = request.POST['txtNombre']
        descripcion = request.POST['txtDescripcion']
        redirectUrl = ''
        test = Test.objects.get(id=idTest)



        if nombre == '':
            messages.add_message(request=request, level = messages.SUCCESS, message="El Nombre es un campo requerido")
            return render(request, 'updateTest.html', {"test" : test} )

        else:
            try:
                test.name = nombre
                test.description = descripcion
                test.save()
                messages.add_message(request=request, level = messages.SUCCESS, message="Test editado correctamente")
                redirectUrl = 'home'
                
            except Exception as e:
                messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al editar el Test")
                return render(request, 'updateTest.html', {"test" : test} )

            return redirect(redirectUrl)
    else:
        return redirect('login2')
