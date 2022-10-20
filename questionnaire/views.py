from unicodedata import name
from django.shortcuts import render, redirect
from questionnaire.models import Alternative, Question, Respuestas_user, Test, TestRegister
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
            return render(request, 'admin/createTest.html')
        else:
            return redirect('login2')
    else:
        return redirect('login2')


@login_required()
def indexCreateTest(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'admin/createTest.html')
    else:
        return redirect('login2')


@login_required()
def indexUpdateTest(request):
    user = request.user
    if user.is_authenticated:
        firstTest = Test.objects.filter()[:1].get()
        if Test.objects.filter(id=firstTest.id).exists():
            test = Test.objects.get(id=firstTest.id)
            questions = Question.objects.filter(test_id = test.id)

            return render(request, 'admin/updateTest.html', {"test" : test, "questions": questions} )
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="No Existe el Test")
            return redirect('home')

    else:
        return redirect('login2')

@login_required()
def indexCreateQuestion(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'admin/createQuestion.html')
    else:
        return redirect('login2')


@login_required()
def viewQuestion(request, idQuestion):
    user = request.user
    if user.is_authenticated:
            question = Question.objects.get(id=idQuestion)
            alternatives = Alternative.objects.filter(question_id = question.id)
            return render(request, 'admin/viewQuestion.html', {"question": question, "alternatives": alternatives} )

    else:
        return redirect('login2')
        
@login_required()
def viewAutoDiagnostic(request):
    user = request.user
    if user.is_authenticated:
        firstTest = Test.objects.filter()[:1].get()
        nodata = True

        testDelated = TestRegister.objects.filter(status=0).delete()
        

        testRegister = TestRegister.objects.create(
            user_id = user.id,
            test_id = firstTest.id,
            status = 0
        )

        if Test.objects.filter(id=firstTest.id).exists():
            test = Test.objects.get(id=firstTest.id)
            questions = Question.objects.filter(test_id = test.id)
            alternatives_selected = {}

            data = []
            
            for question in questions:
                alternatives = Alternative.objects.filter(question_id = question.id)

            for altern in alternatives_selected:
                print('1-')
            return render(request, 'user/autodiagnostic.html', {"test" : test, "questions": questions, "testregister": testRegister} )
        else:
            messages.add_message(request=request, level = messages.SUCCESS, message="No Existe el Test")
            return redirect('home')


@login_required()
def indexViewResult(request, testregister_id):
    user = request.user
    if user.is_authenticated:

        testRegist = TestRegister.objects.get(id=testregister_id)

        return render(request, 'user/termometro.html', {'testRegist': testRegist})
    else:
        return redirect('login2')
        

#Pendiente evaluar validaciones
def addTest(request):
    user = request.user
    if user.is_authenticated:

        nombre = request.POST['txtNombre']
        pretest_text = request.POST['txtPretest']
        redirectUrl = ''

        if nombre == '':
            messages.add_message(request=request, level = messages.SUCCESS, message="El Nombre es un campo requerido")
            redirectUrl = 'createTest'

        else:
            try:
                test = Test.objects.create(
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
        return redirect('login2')




def updateTest(request, idTest):
    user = request.user
    if user.is_authenticated:

        nombre = request.POST['txtNombre']
        pretest = request.POST['txtPretest']
        introduction = request.POST['txtIntroduction']

        redirectUrl = ''
        test = Test.objects.get(id=idTest)



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
        return redirect('login2')



#Agregar pregunta a test
def addCuestion(request):
    user = request.user
    if user.is_authenticated:

        firstTest = Test.objects.filter()[:1].get()
        question = request.POST['txtQuestion']
        type = request.POST['txtType']
        redirectUrl = ''

        if question == '':
            messages.add_message(request=request, level = messages.SUCCESS, message="La Pregunta es un campo requerido")
            redirectUrl = 'createQuestion'

        else:
            try:
                questionAdd = Question.objects.create(
                test = firstTest,
                question_text = question,
                question_type = type
                )

                for x in range(1,5):
                    alternative = Alternative.objects.create(
                        question = questionAdd,
                        alternative = x
                    )

                messages.add_message(request=request, level = messages.SUCCESS, message="Test agregado correctamente")
                return redirect('updateTest')
                
            except Exception as e:
                messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al agregar el Test")
                return redirect('updateTest')
        return redirect(redirectUrl)
    else:
        return redirect('login2')

#Guardar pregunta en primer test
def saveQuestion(request, idQuestion):
    user = request.user
    if user.is_authenticated:

        firstTest = Test.objects.filter()[:1].get()
        question = request.POST['txtQuestion']
        type = request.POST['txtType']
        redirectUrl=''

        questionSave = Question.objects.get(id=idQuestion)

        if question == '':
            messages.add_message(request=request, level = messages.SUCCESS, message="La Pregunta es un campo requerido")
            return redirect('viewQuestion',idQuestion=idQuestion)

        else:
            try:
                questionSave = Question.objects.get(id=idQuestion)
                questionSave.question_text = question
                questionSave.question_type = type
                questionSave.save()

                messages.add_message(request=request, level = messages.SUCCESS, message="Pregunta guardada correctamente")
                return redirect('updateTest')
                
            except Exception as e:
                messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al guardar la pregunta")
                return redirect('viewQuestion',idQuestion=idQuestion)
    else:
        return redirect('login2')


#Agregar pregunta a test
def deleteQuestion(request, idQuestion):
    user = request.user
    if user.is_authenticated:
        firstTest = Test.objects.filter()[:1].get()
        try:
            questionDelete = Question.objects.get(id=idQuestion)
            questionDelete.delete()

            messages.add_message(request=request, level = messages.SUCCESS, message="Pregunta eliminada correctamente")
            return redirect('updateTest')
            
        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al eliminar la pregunta")
            return redirect('viewQuestion',idQuestion=idQuestion)
    else:
        return redirect('login2')


#Guardar pregunta en primer test
def saveResp(request, testRegisterId, questionId):
    user = request.user

    if user.is_authenticated:
        
        alternative = request.POST['flexRadioDefault']
        print(alternative)

        registerSelected = TestRegister.objects.get(id=testRegisterId)
        firstTest = Test.objects.filter()[:1].get()
        questions = Question.objects.filter(test_id = firstTest.id)
        questionSelect = Question.objects.get(id=questionId)
        nodata = False


        testRegister = Respuestas_user.objects.create(
            alternative = alternative,
            testregister = registerSelected,
            question_id = questionId,
            question_text = questionSelect.question_text,
            question_type = questionSelect.question_type

        )

        respuestasSaved = Respuestas_user.objects.filter(testregister_id=testRegisterId)


        listInputSaved = []

        for respuestaSav in respuestasSaved:
            listInputSaved.append(respuestaSav.question_id)
            
        return render(request, 'user/autodiagnostic.html', {"test" : firstTest, "questions": questions, "testregister": registerSelected, "respuestasSaved": listInputSaved} )
   
    else:
        return redirect('login2')

#Agregar pregunta a test
def registerTest(request, testregister_id):
    user = request.user
    if user.is_authenticated:
        firstTest = Test.objects.filter()[:1].get()
        try:

            registerSelected = TestRegister.objects.get(id=testregister_id)
            firstTest = Test.objects.filter()[:1].get()
            questions = Question.objects.filter(test_id = firstTest.id)
            
            respuestasSaved = Respuestas_user.objects.filter(testregister_id=testregister_id)

            listInputSaved = []

            for respuestaSav in respuestasSaved:
                listInputSaved.append(respuestaSav.question_id)


            respuestasUser = Respuestas_user.objects.filter(testregister_id=testregister_id)

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
                else:
                    print("Error al guardar")

            if contadorDepre == 7 and contadorAnsiedad==7 and contadorEstres==7:


                registerSelected.status=1
                registerSelected.result_depresion = sumDepre*2
                registerSelected.result_ansiedad = sumAnsi*2
                registerSelected.result_estres = sumEst*2
                registerSelected.save()
                return redirect('indexViewResult',testregister_id=registerSelected.id)
            else:
                messages.add_message(request=request, level = messages.SUCCESS, message="Porfavor, responda todas las preguntas.")
                return render(request, 'user/autodiagnostic.html', {"test" : firstTest, "questions": questions, "testregister": registerSelected, "respuestasSaved": listInputSaved} )
            
        except Exception as e:
            messages.add_message(request=request, level = messages.SUCCESS, message="Ha ocurrido un error al responder el test")
            return redirect('viewQuestion')
    else:
        return redirect('login2')