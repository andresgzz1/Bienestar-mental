from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('allProfesional/', views.get_All_Profesional, name='allProfesional'),
    path('createProfesional/', views.indexCreateProfesional,name='createProfesional'),
    path('addProfesional/', views.addProfesional, name='addProfesional'),
    path('updateProfesional/<idProfesional>',views.indexUpdateProfesional, name='updateProfesional'),
    path('fun_updateProfesional/<idProfesional>',views.updateProfesional, name='funupdateProfesional'),
    path('deleteProfesional/<idProfesional>',views.deleteProfesional, name='deleteProfesional'),
    path('editarProfesional/<idProfesional>',views.editarProfesional, name='editarProfesional'),
    path('detalleProfesional/<idProfesional>',views.detalleProfesional, name='editarProfesional'),
    path('allProfesionals/', views.get_All_Profesional_user, name='viewuser')
]
