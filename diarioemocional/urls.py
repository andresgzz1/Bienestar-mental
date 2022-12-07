from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
     path('allDiario/',views.get_All_Diario,name="allDiario"),
     path('createDiario/', views.createDiario, name='createDiario'),
     path('createDiariosave/', views.createDiariosave, name='createDiariosave'),
     path('deleteDiario/<idEntrada>', views.deleteDiario, name='deleteDiario'),
     path('viewDiario/', views.viewDiario, name='viewDiario'),
     path('editarDiario/<idEntrada>',views.editarDiario,name='editarDiario'),
     path('fun_updateDiario/<idEntrada>',views.updateDiario,name='funupdateDiario'),
     path('detalleDiario/<idEntrada>',views.detalleDiario,name='detalleDiario')
]