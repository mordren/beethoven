import datetime
from django.db import models
from django.core.management.base import BaseCommand
from atividades.models import Semana, Empresa

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        empresas = Empresa.objects.all()
        num = 0
        for empresa in empresas:   
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
                model = Semana(inicio=inicioQuinzena,fim=fimQuinzena,numero=num,empresa=empresa)
                model.save()
                
                num = num + 1 
                inicioQuinzena = fimQuinzena+ datetime.timedelta(1)
                model = Semana(inicio=inicioQuinzena,fim=lastDay,numero=num,empresa=empresa)
                model.save()
                
            num = 0 