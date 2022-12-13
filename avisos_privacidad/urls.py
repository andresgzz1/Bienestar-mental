from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('cargarArchivo/', views.cargarArchivo, name="cargarArchivo"),
    path('verAvisos/<idavisosPrivacidad>/', views.verAvisos, name='verAvisos'),
    path('deleteAvisos/<idavisosPrivacidad>/',
         views.deleteAvisos, name='deleteAvisos'),
]
