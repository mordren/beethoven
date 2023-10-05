import datetime
from django.db import models
from django.core.management.base import BaseCommand
from analiseProcessos.models import Questao, Semana, Empresa
import pandas as pd
import csv
from pathlib import Path

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        empresas = Empresa.objects.all()
        num = 0
        carregarQuestoes()
        '''
        for empresa in empresas:
            if empresa.PP:
                criarEmpresa(empresa, 'PP')
            if empresa.OIVA:
                criarEmpresa(empresa, 'OIVA')
            if empresa.SV:
                criarEmpresa(empresa, 'SV') 
        '''
       
def criarEmpresa(empresa, portaria):
    num = 0
    for i in range(1,13):
        day = datetime.date(datetime.date.today().year,i,1)
        #uma adaptação pra pegar o ultimo dia do mês
        if (i != 12):
            lastDay = datetime.date(datetime.date.today().year,i+1,1)-datetime.timedelta(1)       
        else:
            lastDay = datetime.date(datetime.date.today().year,1,1)-datetime.timedelta(1)

        inicioQuinzena = day 
        fimQuinzena = day + datetime.timedelta(15)
        
        num = num + 1 
        model = Semana(inicio=inicioQuinzena,fim=fimQuinzena,numero=num,empresa=empresa, portaria=portaria)
        model.save()
        
        num = num + 1 
        inicioQuinzena = fimQuinzena+ datetime.timedelta(1)
        model = Semana(inicio=inicioQuinzena,fim=lastDay,numero=num,empresa=empresa, portaria=portaria)
        model.save()      

def carregarQuestoes():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    with open(BASE_DIR / './static/questoes.csv', 'r', encoding='utf-8') as arquivo:
        arquivo_csv = csv.reader(arquivo, delimiter=';')
        for linha in arquivo_csv:
            questao = Questao.objects.create()
            questao.questao = linha[0]
            questao.portaria = linha[1]
            questao.titulo = linha[2]
            questao.numero = int(linha[3])            
            questao.save()            