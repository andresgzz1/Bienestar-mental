from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
     path('allDiario/',views.get_All_Diario,name="allDiario"),
     path('addEmocion/',views.addEmocion,name='addEmocion'),
     path('createEmocion/',views.indexCreateEmocion,name='createEmocion'),
     path('allEmocion/',views.get_All_Emocion,name="allEmocion"),
     path('updateEmocion/<idEmocion>',views.indexUpdateEmocion,name='updateEmocion'),
     path('fun_updateEmocion/<idEmocion>',views.updateEmocion,name='funupdateEmocion'),
     path('editarEmocion/<idEmocion>',views.editarEmocion,name='editarEmocion'),
     path('deleteEmocion/<idEmocion>',views.deleteEmocion, name='deleteProfesional'),
     path('detalleEmocion/<idEmocion>',views.detalleEmocion,name='detalleEmocion'),
     path('createDiario/', views.createDiario, name='createDiario'),
     path('createDiariosave/', views.createDiariosave, name='createDiariosave'),
     path('deleteDiario/<idEntrada>', views.deleteDiario, name='deleteDiario'),
     path('viewDiario/', views.viewDiario, name='viewDiario'),
     path('editarDiario/<idEntrada>',views.editarDiario,name='editarDiario'),
     path('fun_updateDiario/<idEntrada>',views.updateDiario,name='funupdateDiario'),
     path('detalleDiario/<idEntrada>',views.detalleDiario,name='detalleDiario')
]