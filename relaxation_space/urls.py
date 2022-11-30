from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    # Templates view
    path('adminView_rp/', views.adminView_rp, name='adminView_rp'),
    path('adminView_rp_add/', views.adminView_rp_add, name='adminView_rp_add'),
    path('adminView_rp_delete/<idImage>/', views.adminView_rp_delete, name='adminView_rp_delete'),
    path('adminView_rp_update/<idImage>/', views.adminView_rp_update, name='adminView_rp_update'),
    # Functions view
]
