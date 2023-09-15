from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #path('', cadastroAnalise, name="cadastroAnalise"),   
    #path('cad/<int:id>/', controleProcesso.as_view(), name='controleProcessos'),
    path('', home, name="atividades-home-view"),
    path('cadSemana/<int:id>', cadSemana.as_view(), name="cadSemana-view"),
    path('listAna/<int:semana>', listAna.as_view(), name="listAna-view"),
    path('cadProc/<int:id>/', cadProc.as_view(), name="cadProc-view"),
    path('util/report/<int:id>',report, name="imprimir"),
    path('listSemana',listaSemana.as_view(), name="listSemana-view"),
    path('cadProcessos',cadProcessos, name="cadProcessos-view"),       
]