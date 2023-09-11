import datetime
from django.db import models
from django.core.management.base import BaseCommand
from atividades.models import Semana

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for i in range(1, 53):
            #pego o primeiro dia do ano e seto para começar
            #pego a primeira Semana desse primeiro dia do ano, e vou para 7 dias para frente, talvez algum ano dê problema, mas por hora vai ser assim
            day = datetime.date(datetime.date.today().year,1,1) + datetime.timedelta(i*7)   
            start = day - datetime.timedelta(days=day.weekday())
            end = start + datetime.timedelta(days=6)

            #print(f"Semana : {i} "+ f" começou em: {start}" + f" e terminou: {end}")
            #crio uma array de array.
            #vou criar uma string com esses dados. Dificilmente vou trabalhar com filtros, se precisar mudo.
            model = Semana(inicio=start,fim=end,numero=i)
            model.save()            
    
    