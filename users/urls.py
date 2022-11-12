from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # ENDPOINTS LOGIN
    path('login_api/', views.login_api),
    path('users/', views.get_users),
    path('register/', views.register_api),
    path('allusers/', views.get_Allusers_standard),
    path('logout/', LogoutView.as_view(), name='logout'),
    # TEMPLATES LOGIN AND ROUTES
    path('', views.login_view, name='login2'),
    path('userInfo/', views.viewUser, name='viewUser'),
    path('UserEdit/', views.viewUserEdit, name='viewUserEdit'),
    path('funUserEdit/', views.funUserEdit, name='funUserEdit'),
    
    path('userResults/', views.viewUserResults, name='viewUserResults'),
    path('del_testRegister/<testid>', views.del_testRegister, name='del_testRegister'),
    #ENDPOINTS ADMIN
    path('pageadmin/', views.admin, name='pageadmin'),
    path('ListallUsers/', views.list_All_Userstandart, name='allUsers'),
    path('AddUser/', views.add_userStandard, name='add_userStandard'),



    #ENDPOINTS USER
    path('customer/', views.customer, name='customer'),
    path('register2/', views.register, name='register'),
]
