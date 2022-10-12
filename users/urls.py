from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from . import views 

urlpatterns = [
    path('login/', views.login_api),
    path('users/', views.get_users),
    path('register/',views.register_api),
    path('allusers/', views.get_Allusers_standard),
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('logout2/', , name='logout2'),
    #Separado
    path('login2/', views.login_view, name='login2'),
    path('register2/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('customer/', views.customer, name='customer'),
]