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
    path('detailUser/', views.indexDetailUser, name='detailUser'),
    # ENDPOINTS ADMIN
    path('pageadmin/', views.admin, name='pageadmin'),
    path('ListallUsers/', views.list_All_Userstandart, name='allUsers'),
    path('AddUser/', views.add_userStandard, name='add_userStandard'),
    path('DeleteUser/<userid>', views.delete_userStandard, name='delete_user'),



    # ENDPOINTS USER
    path('customer/', views.customer, name='customer'),
    path('register2/', views.register, name='register'),
]
