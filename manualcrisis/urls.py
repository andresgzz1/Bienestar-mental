from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('indexuploadManual/', views.indexCreateProfesional,name='createProfesional'),
    path('uploadManual/', views.addProfesional, name='addProfesional'),
    path('updateManual/<idManual>',views.indexUpdateProfesional, name='updateProfesional'),
    path('updateManual/<idManual>',views.updateProfesional, name='funupdateProfesional'),
    path('deleteManual/<idManual>',views.deleteProfesional, name='deleteProfesional'),
    path('editarManual/<idManual>',views.editarProfesional, name='editarProfesional'),
    path('deleteManuallist/<idManual>',views.detalleProfesional, name='editarProfesional'),
    path('search/',views.search,name="search")
]
