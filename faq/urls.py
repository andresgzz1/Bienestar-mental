from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # ENDPOINTS LOGIN
     path('faqAdmin/<type>', views.view_adminfaq, name='faqAdmin'),
     path('add_faq/<type>', views.add_faq, name="add_faq"),
     path('edit_faq/<type>/<id>', views.edit_faq, name="edit_faq"),
     path('delfaq/<id>', views.delfaq, name='delfaq'),
     path('view_faq/', views.view_faq, name='faqAdmin')
]
