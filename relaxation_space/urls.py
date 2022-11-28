from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    # Templates view
    path('adminView_rp/', views.adminView_rp, name='adminView_rp'),
    # Functions view
]
