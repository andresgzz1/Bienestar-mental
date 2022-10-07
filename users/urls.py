from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_api),
    path('users/', views.get_users),
    path('register/',views.register_api)
]