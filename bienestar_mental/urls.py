"""bienestar_mental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', include('home.urls'), name='home'),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('questionnaire/', include('testdass.urls')),
    path('faq/', include('faq.urls')),
    path('profesional/', include('profesional.urls')),
<<<<<<< HEAD
    path('diarioemocional/', include('diarioemocional.urls')),
=======
    #path('diario_emocional/',include('diario_emocional.urls')),
>>>>>>> origin
    path('relaxation_space/',include('relaxation_space.urls')),
    path('config_web/',include('config_web.urls')),
    # Reset password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="user/reset_pass.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="user/reset_pass_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/reset_pass_reset.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="user/reset_pass_complete.html"), name="password_reset_complete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
