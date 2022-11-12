from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
     path('addEmocion/',views.addEmocion,name='addEmocion'),
     path('createEmocion/',views.indexCreateEmocion,name='createEmocion'),
     path('allEmocion/',views.get_All_Emocion,name="allEmocion"),
     path('updateEmocion/<idEmocion>',views.indexUpdateEmocion,name='updateEmocion'),
     path('fun_updateEmocion/<idEmocion>',views.updateEmocion,name='funupdateEmocion'),
     path('editarEmocion/<idEmocion>',views.editarEmocion,name='editarEmocion'),
     path('deleteEmocion/<idEmocion>',views.deleteEmocion, name='deleteProfesional'),
     path('detalleEmocion/<idEmocion>',views.detalleEmocion,name='detalleEmocion')
]
