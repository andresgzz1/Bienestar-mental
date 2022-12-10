from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    # Templates view
    # Administración de espacios de relajación (Imagenes)
    path('adminView_rp/', views.adminView_rp, name='adminView_rp'),
    path('adminView_rp_add/', views.adminView_rp_add, name='adminView_rp_add'),
    path('adminView_rp_delete/<idImage>/',
         views.adminView_rp_delete, name='adminView_rp_delete'),
    path('adminView_rp_update/<idImage>/',
         views.adminView_rp_update, name='adminView_rp_update'),
    # Administración de espacios de relajación (Gifs)
    path('adminView_rp_gif/<idSpace>/',
         views.adminView_rp_gif, name='adminView_rp_gif'),
    path('rp_gif_add/<idSpace>/', views.rp_gif_add, name='rp_gif_add'),
    path('rp_gif_delete/<idGif>/', views.rp_gif_delete, name='rp_gif_delete'),
    path('rp_gif_edit/<idGif>/', views.rp_gif_edit, name='rp_gif_edit'),
    # Administración de espacios de relajación (sound)
    path('adminView_rp_sound/<idsound>/',views.adminView_rp_sounds, name='adminView_rp_sound'),
    path('add_sound_rp/<idsound>/', views.add_sound_rp, name='add_sound_rp'),
    path('delete_sound_rp/<idsound>/',views.delete_sound_rp, name='delete_sound_rp'),
    path('update_sound_rp/<idsound>/',views.update_sound_rp, name='update_sound_rp'),
    # Template principal de espacios de relajación
    path('relax_space_view/<type>',
         views.relax_space_view, name='relax_space_view'),
    # Functions view
]
