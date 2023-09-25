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
    path('listAna/<int:semana>/', login_required(listAna.as_view()), name="listAna-view"),
    path('updProc/<int:id>/', login_required(updProc.as_view()), name="updProc-view"),
    path('util/report/<int:id>/', report, name="imprimir"),
    path('listSem/', login_required(listSem.as_view()), name="listSem-view"),
    path('cadProc/', cadProc, name="cadProc-view"),       
]