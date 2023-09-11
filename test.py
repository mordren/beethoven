from datetime import date, timedelta
import datetime
semanas = []

for i in range(1, 53):
    #pego o primeiro dia do ano e seto para começar
    #pego a primeira semana desse primeiro dia do ano, e vou para 7 dias para frente, talvez algum ano dê problema, mas por hora vai ser assim
    day = datetime.date(datetime.date.today().year,1,1) + timedelta(i*7)   
    start = day - timedelta(days=day.weekday())
    end = start + timedelta(days=6)
    
    #print(f"Semana : {i} "+ f" começou em: {start}" + f" e terminou: {end}")
    #crio uma array de array.
    #vou criar uma string com esses dados. Dificilmente vou trabalhar com filtros, se precisar mudo.
    semana = (f"Semana: {i} - "+start.strftime("%d/%m/%y")+" - "+end.strftime("%d/%m/%y"))
    #semana = [start, end]
    print(semana)
    semanas.append(semana)

    