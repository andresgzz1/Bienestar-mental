
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from users.models import User, userStandard
from .serializers import  RegisterSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import requests
# Create your views here.



# Enpoint para login
@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data= request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info':{
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
        'user_info':{
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
                    user_list= userStandard.objects.all()
                    user_json=[]
                    for h in user_list:
                        user_json.append({'username': h.user.username, 'id': h.id, 'email': h.email})
                    return Response({'Listado': user_json })
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
    
    print(user)

    userStandard.objects.create(
            user = user.pk,
            rut = '1212-2',
            phone = '98888'
        )

    _, token = AuthToken.objects.create(user)

    return Response({
        'token': token
    })
    


"""  -------------------------------  """

from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    return render(request, 'index.html')

# Registrar usuario
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            form.save(commit=False)

            print(form.cleaned_data)

            user_1 = User(
            username = form.cleaned_data['username'],
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            email = form.cleaned_data['email'],
            is_client = True,
            is_admin = False
            )

            user_1.set_password(form.cleaned_data['password1'])
            user_1.save()

            user_standard = userStandard.objects.create(
            user = user_1,
            matricula = form.cleaned_data['matricula'],
            phone = form.cleaned_data['phone'],
            sexo = form.cleaned_data['sexo']
            )

            user_standard.save()

            msg = 'user created'
            return redirect('login2')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})

# Iniciar Sesion
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_client:
                login(request, user)
                return redirect('customer')

            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def logout_view(request):
    msg = None

    user = request.user

    if user.is_authenticated:
        logout(request)
        msg= 'logout ok'
    else:
        msg= 'invalid credentials'


    return render(request, 'login.html', {'msg': msg})

@login_required(login_url="login2")
def admin(request):
    user = request.user
    #url = 'http://127.0.0.1:8000/questionnaire/allTest'
    #data = requests.get(url)
    #print(data)
    if user is not None and user.is_admin:
        return render(request,'admin.html')
    else:
        return redirect('login2')
    
    
# endpoint para ingresar al template de usuario
@login_required(login_url="login2")
def customer(request):

    
    """ token = request.auth.key
    print(token) """

    user = request.user
    url = 'http://127.0.0.1:8000/questionnaire/allTest'
    data2 = requests.get(url,headers={'Authorization':"Token myToken"})
    print(data2.json())
    user = request.user
    if user is not None and user.is_client:
        return render(request,'customer.html')
    else:
        return redirect('login2')