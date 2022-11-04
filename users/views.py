from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect
from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from users.models import User, userStandard
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from profesional.views import es_correo_valido
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
def indexDetailUser(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'detail_user.html')
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
                    request=request, level=messages.ERROR, message="Username is already used")
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
