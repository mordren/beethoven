from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #path('', cadastroAnalise, name="cadastroAnalise"),   
    #path('cad/<int:id>/', controleProcesso.as_view(), name='controleProcessos'),
    path('', login_required(home), name="atividades-home-view"),
    path('cadSem/<int:id>/', login_required(cadSem.as_view()), name="cadSem-view"),    
    path('listSem/', login_required(listSem.as_view()), name="listSem-view"),
    path('updNumProc/', updNumProc, name="updNumProc-view"),
     
    path('util/report/<int:id>/', report, name="imprimir"),
    
    path('cadProc/', cadProc, name="cadProc-view"),       
    path('listProc/<int:semana>/', login_required(listProc.as_view()), name="listProc-view"),
    path('updProc/<int:id>/', login_required(updProc.as_view()), name="updProc-view"),
    path('delProc/<int:id>/', delProc, name="delProc-view"),
    path('newProc/<int:semana>/', newProc, name="newProc-view"),
]