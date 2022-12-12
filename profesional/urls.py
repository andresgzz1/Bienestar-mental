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
    path('fun_updateimagenProfesional/<idProfesional>',views.updateImagenProfesional, name='funupdateimagenProfesional'),
    path('editarimagenProfesional/<idProfesional>',views.editarimagenProfesional, name='editarimagenProfesional'),
    path('detalleProfesional/<idProfesional>',views.detalleProfesional, name='editarProfesional'),
    path('detalleprofesionalUser/<idProfesional>',views.detalleprofesionalUser, name='detalleprofesionalUser'),
    path('allProfesionals/', views.get_All_Profesional_user, name='allProfesionals'),
    path('search/',views.search,name="search"),
    path('searchf/',views.searchf,name="searchf")
]
