from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
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



@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    return Response({
        'token': token
    })
    