from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from . import views 

urlpatterns = [
       path('updateTest/', views.indexUpdateTest, name='updateTest'),
       path('fun_updateTest/<idTest>', views.updateTest, name='funupdateTest'),
       path('viewQuestion/<idQuestion>', views.viewQuestion, name='viewQuestion'),
       path('createQuestion/', views.indexCreateQuestion, name='createQuestion'),
       path('addQuestion/', views.addCuestion, name='addQuestion'),
       path('saveQuestion/<idQuestion>', views.saveQuestion, name='saveQuestion'),
       path('deleteQuestion/<idQuestion>', views.deleteQuestion, name='deleteQuestion'),
       path('autoDiagnostic/', views.viewAutoDiagnostic, name='viewAutoDiagnostic'),
       path('saveResp/<testRegisterId>/<questionId>', views.saveResp, name='saveResp'),
       path('registerTest/<testregister_id>', views.registerTest, name='registerTest'),
       path('indexViewResult/<testregister_id>', views.indexViewResult, name="indexViewResult"),
       path('indexIntroTest/', views.indexIntroTest, name='indexIntroTest'),
       path('viewResp_test/<testreg_id>', views.viewResp_test, name='viewResp_test'),
       #Recomendation (techniques)
       path('viewRecomendation/<disorder>/<level>/<testregister_id>',views.viewRecomendation, name='viewRecomendation'),
       path('viewRecomendationAdmin/<disorder>/<level>',views.viewRecomendationAdmin, name='viewRecomendationAdmin'),
       path('viewRecomendationAll/<filterType>/<filterOrden>',views.viewRecomendationAll, name='viewRecomendationAll'),
       path('viewRecomendationFilter/', views.viewRecomendationFilter, name='viewRecomendationFilter'),
       path('saveTechniques/<id_relaxation_tech>', views.saveTechniques , name= 'saveTechniques'),
       path('deleteTechniques/<id_relaxation_tech>/<id_link>', views.deleteLinkRecomendation , name= 'deleteLinkRecomendation'),
       path('funfilterLinks/<disorder>/<level>',views.funFilterLinks,name='funFilterLinks'),
       path('addLinkRecomendation/<id_relaxation_tech>', views.addLinkRecomendation, name = 'addLinkRecomendation'),
       path('editLinkRecomendation/<id_relaxation_tech>/<id_link>', views.editLinkRecomendation, name = 'editLinkRecomendation'),


]
