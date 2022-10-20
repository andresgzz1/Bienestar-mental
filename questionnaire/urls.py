from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from . import views 

urlpatterns = [
       path('allTest/', views.get_All_Test),
       path('createTest/', views.indexCreateTest, name='createTest'),
       path('addTest/', views.addTest, name='addTest'),
       path('updateTest/', views.indexUpdateTest, name='updateTest'),
       path('fun_updateTest/<idTest>', views.updateTest, name='funupdateTest'),
       path('viewQuestion/<idQuestion>', views.viewQuestion, name='viewQuestion'),
       path('createQuestion/', views.indexCreateQuestion, name='createQuestion'),
       path('addQuestion/', views.addCuestion, name='addQuestion'),
       path('saveQuestion/<idQuestion>', views.saveQuestion, name='saveQuestion'),
       path('deleteQuestion/<idQuestion>', views.deleteQuestion, name='deleteQuestion'),
       path('autoDiagnostic/', views.viewAutoDiagnostic, name='viewAutoDiagnostic'),
       path('saveResp/<testRegisterId>/<questionId>', views.saveResp, name='saveResp')
]
