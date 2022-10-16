from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from . import views 

urlpatterns = [
       path('allProfesional/', views.get_All_Profesional),
       path('createProfesional/', views.indexCreateProfesional, name='createProfesional'),
       path('addProfesional/', views.addProfesional, name='addProfesional'),
       path('updateProfesional/', views.indexUpdateProfesional, name='updateTest'),
       path('fun_updateProfesional/<idProfesional>', views.updateProfesional, name='funupdateProfesional')
]