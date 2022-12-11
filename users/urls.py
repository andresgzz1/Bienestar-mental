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
    path('userResults/<idUser>/<filter>',
         views.viewUserResults, name='viewUserResults'),
    path('filterUserResults/<idUser>',
         views.filterUserResults, name='filterUserResults'),
    path('del_testRegister/<testid>/',
         views.del_testRegister, name='del_testRegister'),
     path('del_user/', views.del_user, name='del_user'),
    # ENDPOINTS ADMIN
    path('pageadmin/', views.admin, name='pageadmin'),
    path('ListallUsers/<filteruser>',
         views.list_All_Userstandart, name='allUsers'),
    path('AddUser/', views.add_userStandard, name='add_userStandard'),
    path('DeleteUser/<userid>', views.delete_userStandard, name='delete_user'),
    path('update_user/<userid>', views.indexUpdateUser, name='update_user'),
    path('fun_updateUser/<userid>',
         views.update_userStandard, name='funupdateUser'),
    path('EditUser/<userid>', views.editarUserstand, name="edit_user"),
    path('filteruser/', views.filter_users, name='filterUser'),
    path('viewSoporte/', views.viewSoporte, name='viewSoporte'),

    # ENDPOINTS USER
    path('customer/', views.customer, name='customer'),
    path('register2/', views.register, name='register'),
]
