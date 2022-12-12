from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('subirManual/', views.subirManual, name="subirManual"),
    path('mirarPDF/<idManual>/', views.mirarPDF, name='mirarPDF'),
    path('eliminarPDF/<idManual>/', views.eliminarPDF, name='eliminarPDF'),
]
