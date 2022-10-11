from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from users.models import User, userStandard
from .serializers import  RegisterSerializer
from rest_framework import status

# Create your views here.


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
                    cuadrilla_list= userStandard.objects.all()
                    cuadrilla_json=[]
                    for h in cuadrilla_list:
                        cuadrilla_json.append({'username': h.user.username, 'rut': h.rut, 'phone': h.phone})
                    return Response({'Listado': cuadrilla_json })
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
from django.contrib.auth import authenticate, login
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            user_standard = userStandard.objects.create(
            user = user,
            rut = '1212-2',
            phone = '98888'
            )

            user_standard.save()

            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


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


def admin(request):
    return render(request,'admin.html')


def customer(request):
    return render(request,'customer.html')


def employee(request):
    return render(request,'employee.html')