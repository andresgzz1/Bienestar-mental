from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('uploadfile/', views.uploadFile, name="uploadFile"),
]
