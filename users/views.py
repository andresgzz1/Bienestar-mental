from django.contrib.auth import authenticate, login, logout

from users import models
from .forms import SignUpForm, LoginForm, editUserForm
from django.shortcuts import render, redirect
from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from users.models import User, userStandard
from questionnaire.models import TestRegister
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from profesional.views import es_correo_valido
from datetime import date, datetime
# Create your views here.

# Enpoint para login


@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'token': token
    })

# Endpoint para tomar al usuario al iniciar sesion


@api_view(['GET'])
def get_users(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    else:
        return Response({'error:': 'Usuario no autenticado'})


@api_view(['GET'])
def get_Allusers_standard(request, format=None):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            if user.is_admin:
                try:
                    user_list = userStandard.objects.all()
                    user_json = []
                    for h in user_list:
                        user_json.append(
                            {'username': h.user.username, 'id': h.id, 'email': h.email})
                    return Response({'Listado': user_json})
                except ValueError:
                    return Response({'Msj': "Valor erroneo"})
                except KeyError:
                    return Response({'Msj': "Error de llave"})
            else:
                return Response({'Msj': "No tienes sifucientes permisos"})
    else:
        return Response({'Msj': "Error metodo no soportado"})


@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    userStandard.objects.create(
        user=user.pk,
        rut='1212-2',
        phone='98888'
    )

    _, token = AuthToken.objects.create(user)

    return Response({
        'token': token
    })


"""  -------------------------------  """

# Create your views here.


def index(request):
    return render(request, 'index.html')


@login_required()
def viewUser(request):
    user = request.user
    if user.is_authenticated:
        if user.is_client:
            userStand = userStandard.objects.get(user_id=user.id)
            userSelect = {'id': user.id, 'username': user.username, 'first_name': user.first_name,
                         'last_name': user.last_name, 'email': user.email, 'matricula': userStand.matricula,'created_at': user.date_joined, 'phone': userStand.phone, 'sexo':userStand.sexo, 'ubicacion': userStand.ubication,'fecha_nacimiento': userStand.birth_date}

            return render(request, 'user/profil.html', {'userSelect':userSelect})
        else:
            return redirect('login2')
    else:
        return redirect('login2')

@login_required()
def viewUserEdit(request):
    user = request.user
    if user.is_authenticated:
        if user.is_client:
            
            userStand = userStandard.objects.get(user_id=user.id)
            userSelect = {'username': user.username, 'first_name': user.first_name,
                        'last_name': user.last_name, 'email': user.email, 'matricula': userStand.matricula,'created_at': user.date_joined, 'phone': userStand.phone, 'sexo':userStand.sexo, 'ubicacion': userStand.ubication,'fecha_nacimiento': userStand.birth_date}
            return render(request, 'user/profilEdit.html', {'userSelect':userSelect})
        else:
            return redirect('login2')
    else:
        return redirect('login2')


@login_required()
def viewUserResults(request, idUser, filter):
    user = request.user
    userComparacion = User.objects.get(id = idUser)

    if user.is_authenticated:
        testsRegister_list = []
        if user.is_client and (user == userComparacion):
            if TestRegister.objects.filter(user_id = user.id).exists():
                """ Mostrar todos los registros """
                testsRegister = TestRegister.objects.filter(user_id = user.id).order_by('-created_at')
                
                """ Filtrar por día """
                if filter == 'day':
                    for testR in testsRegister:
                        if testR.created_at.date() == datetime.now().date():
                            testsRegister_list.append(testR)
                            print("True")
                        else:
                            print("False")
                """ Filtrar por mes """
                if filter == 'month':
                    for testR in testsRegister:
                        fechaTest = testR.created_at.date()
                        fechaActual = datetime.now().date()
                        if fechaTest.year == fechaActual.year and fechaActual.month == fechaTest.month:
                            testsRegister_list.append(testR)
                            print("True")
                        else:
                            print("False")
                """ Filtrar todos """
                if filter == 'all':
                    testsRegister_list.extend(testsRegister)
                """ Filtrar hace una semana """
                if filter == 'week':
                    for testR in testsRegister:
                        fechaTest = testR.created_at.date()
                        fechaActual = datetime.now().date()
                        if ((fechaActual.day - 6) <= fechaTest.day <= fechaActual.day) and fechaActual.month == fechaTest.month:
                            testsRegister_list.append(testR)
                            print("True")
                        else:
                            print("False")
         
            else:
                testsRegister = []
            return render(request, 'user/profilResults.html', {'testsRegister': testsRegister_list, 'user': userComparacion, 'filter': filter})
        elif user.is_admin:
            if TestRegister.objects.filter(user_id = idUser).exists():
                testsRegister = TestRegister.objects.filter(user_id = idUser).order_by('-created_at')
                """ Filtrar por día """
                if filter == 'day':
                    for testR in testsRegister:
                        if testR.created_at.date() == datetime.now().date():
                            testsRegister_list.append(testR)
                            print("True")
                        else:
                            print("False")
                """ Filtrar por mes """
                if filter == 'month':
                    for testR in testsRegister:
                        fechaTest = testR.created_at.date()
                        fechaActual = datetime.now().date()
                        if fechaTest.year == fechaActual.year and fechaActual.month == fechaTest.month:
                            testsRegister_list.append(testR)
                            print("True")
                        else:
                            print("False")
                """ Filtrar todos """
                if filter == 'all':
                    testsRegister_list.extend(testsRegister)
                """ Filtrar hace una semana """
                if filter == 'week':
                    for testR in testsRegister:
                        fechaTest = testR.created_at.date()
                        fechaActual = datetime.now().date()
                        if ((fechaActual.day - 6) <= fechaTest.day <= fechaActual.day) and fechaActual.month == fechaTest.month:
                            testsRegister_list.append(testR)
                            print("True")
                        else:
                            print("False")
                """ Filtros """

            else:
                testsRegister = []

            return render(request, 'user/profilResults.html', {'testsRegister': testsRegister_list, 'user': userComparacion, 'filter': filter})            
        else:
            messages.add_message(
                request=request, level=messages.ERROR, message="No puedes ver los registros")
            return redirect('login2')
    else:
        return redirect('login2')


""" Filtrar lista de resultados """

login_required()
def filterUserResults(request, idUser):
    user = request.user
    if user.is_authenticated:        
        filterType = request.POST.get('txtFilter')
        filterTypeValue = ""
        """ Type """
        if filterType == None:
            filterTypeValue = "all"
        if filterType == 'all':
            filterTypeValue = "all"
        if filterType == 'day':
            filterTypeValue = "day"
        if filterType == 'month':
            filterTypeValue = "month"
        if filterType == 'week':
            filterTypeValue = "week"



        return redirect('viewUserResults',idUser,filterTypeValue)

    else: 
        return redirect('login2')


# Registrar usuario
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            form.save(commit=False)

            user_1 = User(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                is_client=True,
                is_admin=False
            )

            user_1.set_password(form.cleaned_data['password1'])
            user_1.save()

            user_standard = userStandard.objects.create(
                user=user_1,
                matricula=form.cleaned_data['matricula'],
                phone=form.cleaned_data['phone'],
                sexo=form.cleaned_data['sexo']
            )

            user_standard.save()
            messages.add_message(
                request=request, level=messages.SUCCESS, message="Usuario creado con exito")
            msg = 'user created'
            return redirect('login2')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'user/register.html', {'form': form, 'msg': msg})


# Iniciar Sesion
def login_view(request):
    user = request.user

    if user.is_authenticated:
        if user.is_client:
            return redirect('customer')
        if user.is_admin:
            return redirect('pageadmin')
    else:
        form = LoginForm(request.POST or None)
        msg = None
        if request.method == 'POST':

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                if username == '' or password == '':
                    msg = 'Los campos son requeridos'
                else:
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_admin:
                        login(request, user)
                        return redirect('pageadmin')
                    elif user is not None and user.is_client:
                        login(request, user)
                        return redirect('customer')
                    else:
                        msg = 'Credenciales invalidas'
            else:
                msg = 'Error al validar forumulario'
        return render(request, 'user/login.html', {'form': form, 'msg': msg})


def logout_view(request):
    msg = None
    user = request.user
    if user.is_authenticated:
        logout(request)
        msg = 'logout ok'
    else:
        msg = 'invalid credentials'
    return render(request, 'login.html', {'msg': msg})


@login_required(login_url="login2")
def admin(request):
    user = request.user
    if user is not None and user.is_admin:
        return render(request, 'admin/admin.html')
    else:
        return redirect('login2')


# endpoint para ingresar al template de usuario
@login_required(login_url="login2")
def customer(request):
    user = request.user
    if user is not None and user.is_client:
        return render(request, 'user/customer.html')
    else:
        return redirect('login2')


# listar usuarios creados vista admin

def list_All_Userstandart(request, format=None):
    user = request.user
    if user.is_authenticated:
        users_all = User.objects.filter(is_superuser=0)
        users = []
        for u in users_all:
            if userStandard.objects.filter(user_id=u.id).exists():
                userStand = userStandard.objects.filter(user_id=u.id)[:1].get()
            else:
                userStand = userStandard(
                    matricula='n/a'
                )

            users.append({'username': u.username, 'first_name': u.first_name,
                         'last_name': u.last_name, 'email': u.email, 'matricula': userStand.matricula})
            print(u)

        return render(request, 'admin/admin-usuario.html', {'users': users})
    else:
        return redirect('login2')


# funcion para añadir nuevo usuario desde admin
def add_userStandard(request):
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            matricula = request.POST['matricula']
            username = request.POST['Username']
            if User.objects.filter(username=username).exists():
                messages.add_message(
                    request=request, level=messages.ERROR, message="Username is already exist")
                return redirect('allUsers')

            first_name = request.POST['First_Name']
            last_name = request.POST['Last_name']
            email = request.POST['email']
            if email != '' and es_correo_valido(email) == False:
                messages.add_message(
                    request=request, level=messages.ERROR, message="Ha ingresado un correo inválido")
                return redirect('allUsers')
            else:
                userStan = User.objects.create(

                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                return redirect('allUsers')
        else:
            messages.add_message(
                request=request, level=messages.ERROR, message="Do not Have permissions")
            return('customer')
    else:
        return redirect('login2')


@login_required()
def funUserEdit(request):
    user = request.user
    if user.is_authenticated:
        if user.is_client:
            userStand = userStandard.objects.get(user_id=user.id)

            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            ubication = request.POST['ubi']
            nacimiento = request.POST['nacimiento']
            nacimiento_date = datetime.strptime(nacimiento, '%Y-%m-%d') 

            if User.objects.filter(username__exact=username).exists() and not User.objects.filter(username__exact=username).filter(id=user.id).exists():
                messages.add_message(request=request, level=messages.ERROR, message="El nombre de usuario ingresado ya está asignado a un usuario")
            elif userStandard.objects.filter(phone__exact=phone).exists() and not userStandard.objects.filter(phone__exact=phone).filter(user_id=user.id).exists():
                messages.add_message(request=request, level=messages.ERROR, message="El número de contacto ingresado ya está asignado a un usuario")
            elif User.objects.filter(email__iexact=email).exists() and not User.objects.filter(email__iexact=email).filter(id=user.id).exists():
                messages.add_message(request=request, level=messages.ERROR, message="El correo ingresado ya está asignado a un usuario")
            elif User.objects.filter(email__iexact=email).exists() and not User.objects.filter(email__iexact=email).filter(id=user.id).exists():
                messages.add_message(request=request, level=messages.ERROR, message="El correo ingresado ya está asignado a un usuario")
            else:
                user.username = username
                user.first_name = first_name
                user.phone = phone
                user.email = email
                userStand.ubication = ubication
                userStand.birth_date = nacimiento_date
                user.save()
                userStand.save()
                messages.add_message(request=request, level=messages.ERROR, message="Guardado correctamente")
                userSelect = {'username': user.username, 'first_name': user.first_name,
                            'last_name': user.last_name, 'email': user.email, 'matricula': userStand.matricula,'created_at': user.date_joined, 'phone': userStand.phone, 'sexo':userStand.sexo, 'ubicacion': userStand.ubication,'fecha_nacimiento': userStand.birth_date}
                print(userSelect)
                return render(request, 'user/profilEdit.html', {'userSelect':userSelect})
            
            userSelect = {'username': username, 'first_name': first_name,
                            'last_name': last_name, 'email': user.email, 'matricula': userStand.matricula,'created_at': user.date_joined, 'phone': userStand.phone, 'sexo':userStand.sexo, 'ubicacion': ubication,'fecha_nacimiento': nacimiento_date}
            
            print(userSelect)
            return render(request, 'user/profilEdit.html', {'userSelect':userSelect})
        else:
            return redirect('login2')
    else:
        return redirect('login2')


#nueva funcion

#Función para eliminar recomendación

# funcion para añadir nuevo usuario desde admin
def del_testRegister(request, testid):
    user = request.user
    if user.is_authenticated:
        if not user.is_admin:
            testDel1 = TestRegister.objects.get(id=testid)
            try:
                testDel = TestRegister.objects.filter(id=testid).delete()
                msj = f"Eliminado correctamente test con fecha: {testDel1.created_at }"
                messages.add_message(request=request, level=messages.ERROR, message=msj)
                return redirect('viewUserResults')
            except Exception as e:
                msj = f"No se pudo eliminar el test con fecha: {testDel1.created_at }"
                messages.add_message(request=request, level=messages.ERROR, message=msj) 
                return redirect('viewUserResults')
        else:
            messages.add_message(
                request=request, level=messages.ERROR, message="Do not Have permissions")
            return redirect('viewUserResults')
    else:
        return redirect('login2')