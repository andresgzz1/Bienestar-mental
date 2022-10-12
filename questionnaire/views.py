from django.shortcuts import render

from questionnaire.models import Test
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

# 
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


