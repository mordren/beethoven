from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #path('', cadastroAnalise, name="cadastroAnalise"),   
    #path('cad/<int:id>/', controleProcesso.as_view(), name='controleProcessos'),
    path('', login_required(home), name="atividades-home-view"),
    path('cadSemana/<int:id>', login_required(cadSemana.as_view()), name="cadSemana-view"),
    path('listAna/<int:semana>', login_required(listAna.as_view()), name="listAna-view"),
    path('cadProc/<int:id>/', login_required(cadProc.as_view()), name="cadProc-view"),
    path('util/report/<int:id>', report, name="imprimir"),
    path('listSemana', login_required(listaSemana.as_view()), name="listSemana-view"),
    path('cadProcessos', cadProcessos, name="cadProcessos-view"),       
]