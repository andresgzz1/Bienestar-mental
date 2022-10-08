from django.urls import path
from . import views

urlpatterns = [
    #path('login/', views.login_api),
    path('users/', views.get_users),
    path('register/',views.register_api),
    
    #Separado
    path('login/', views.login_view, name='login_view'),
    path('register2/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('customer/', views.customer, name='customer'),
    path('employee/', views.employee, name='employee'),
]