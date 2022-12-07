from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    # Templates view
    # Administración de espacios de relajación (Imagenes)
    path('adminView_rp/', views.adminView_rp, name='adminView_rp'),
    path('adminView_rp_add/', views.adminView_rp_add, name='adminView_rp_add'),
    path('adminView_rp_delete/<idImage>/', views.adminView_rp_delete, name='adminView_rp_delete'),
    path('adminView_rp_update/<idImage>/', views.adminView_rp_update, name='adminView_rp_update'),
    # Administración de espacios de relajación (Gifs)
    path('adminView_rp_gif/<idSpace>/', views.adminView_rp_gif, name='adminView_rp_gif'),
    path('rp_gif_add/<idSpace>/', views.rp_gif_add, name='rp_gif_add'),
    # Template principal de espacios de relajación
    path('relax_space_view/', views.relax_space_view, name='relax_space_view'),
    # Functions view
]