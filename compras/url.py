from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required


urlpatterns = [
    #path('', cadastroAnalise, name="cadastroAnalise"),   
    #path('cad/<int:id>/', controleProcesso.as_view(), name='controleProcessos')
    path('cadCompra', login_required(CadCompra.as_view()), name="cadCompra-view"),
    path('listCompra', login_required(ListCompra.as_view()), name="listCompra-view"),
    path('deleteCompra/<int:id>/', compraDelete, name="deleteCompra-view"),
    path('updateCompra/<int:id>/', login_required(UpdateCompra.as_view()), name="updateCompra-view"),
    path('util/reportCompra/<int:id>/', report, name="imprimirCompra"),
]