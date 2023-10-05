from django.db import models
from user.models import Empresa
from datetime import date, timedelta
import datetime

# Create your models here.

class Semana(models.Model):
    inicio = models.DateField()
    fim = models.DateField()
    numero = models.IntegerField()
    processos = models.IntegerField(default=0)
    analises = models.IntegerField(default=0)
    realizado = models.BooleanField(default=False)
    data = models.DateField(default=date.today)
    numeroNC = models.IntegerField(default=0)
    portaria = models.CharField(max_length=4, choices=[("SV","SV"), ('OIVA', 'OIVA'),("PP", 'PP')], default="SV", null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
            
    def __str__(self):
        return (f"Semana: {self.numero} - "+self.inicio.strftime("%d/%m/%y")+"-"+self.fim.strftime("%d/%m/%y")+' - '+self.empresa.nome)
   
class AnaliseProcessoSV(models.Model):
    semana = models.ForeignKey(Semana, on_delete=models.CASCADE)
    OS = models.IntegerField(help_text="Nº da OS", null=True)
    data = models.DateField(default=date.today)
    user = models.CharField(max_length=30, default="João")
    crlv = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="1)	CRLV ou CRV ou NF compra veículo – HABILITAÇÃO do condutor", null=True)
    decalque = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="2)	DECALQUE do número do chassi;", null=True)
    vistoriaInicial = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A",  help_text="3)	FOR ADM 31 ORDEM DE SERVIÇO com a VISTORIA INICIAL;", null=True)
    verificaoEscopo = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')],default="A", help_text="4)	Lista de verificação correta ao escopo, rastreável, com anotações corretas, correções conforme procedimento, com quantificáveis rastreado ao equipamento entre outros;", null=True)
    linhaInspecao = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')],default="A", help_text="5)	Relatório da LINHA DE INSPEÇÃO, assinado por todos, 'A', com número de patrimônio, rastreavel ao veículo, equipamento calibrado entre outros;", null=True)
    opacidade = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')],default="A", help_text="6)	Relatório de OPACIDADE, ANÁLISE DE GASES quando aplicável, assinado por todos, 'A', com número de patrimônio, rastreavel ao veículo, equipamento calibrado entre outros;", null=True)
    ruido = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')],default="A", help_text="7)	Relatório de RUÍDO, quando aplicável, assinado por todos, 'A', com número de patrimônio, rastreavel ao veículo, equipamento calibrado entre outros;", null=True)
    naoConformidade = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')],default="A", help_text="8)	Registro de NÃO CONFORMIDADE;", null=True)
    rasurasProcessos = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')],default="A", help_text="9)	Verificar a existência de RASURAS NOS PROCESSOS;", null=True)
    registrosFotograficos = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A",help_text="10)	Registro fotográfico do EIXO (s) DIANTEIRO (s) e EIXO (s) TRASEIRO (s) do veículo e a banda de rodagem dos pneus dianteiros e pneus traseiros. A foto do eixo dianteiro deve ser tirada no sentido do eixo traseiro, a foto do eixo traseiro deve ser tirada no sentido do eixo dianteiro, quando houver um terceiro eixo, o registro fotográfico deve ser tirado no sentido do eixo traseiro; Registro fotográfico do Para todos os veículos com PARA-CHOQUE homologados, um (1) registro fotográfico da plaqueta de homologação do pára-choque; Registro fotográfico do transversal do PINO-REI e de sua MESA LIMPOS ou QUINTA RODA, quando aplicável; Registro fotográfico das LATERAIS DOS VEÍCULOS com as FAIXAS REFLETIVAS, quando aplicáveis; Registro fotográfico ALÍVIO DE PESO no eixo direcional em veículos pesados, quando aplicável; Registro fotográfico da TRASEIRA DO VEÍCULO na linha de inspeção mecanizada, que tenha possibilidade de leitura da PLACA de licença no RELATÓRIO DE INSPEÇÃO.Obs. Os registros fotográficos devem conter data e hora.", null=True)
    filmagem = models.CharField(max_length=2, choices=[('A','A'),('R', 'R'),('NA', 'NA')],default="A", help_text="11)	Filmagem de todas as etapas de inspeção, verificar calibragem de pneus, ensaio de regloscopio, verificação do sistema de sinalização, ensaio de opacidade e ruído, dentre outros, a filmagem deve conter data e horas no formato (DD/MM/AAAA) e (hh:mm:ss).", null=True)
    observacoes = models.TextField(help_text="Observações", null=True)
    realizado = models.BooleanField(default=False)
    NC = models.CharField(max_length=3, choices=[('Sim', 'Sim'),("Não","Não")], default="Não")
    
    def __str__(self):
        if self.realizado == True:
            return str(self.OS)
        else:
            return "Análise a realizar, clique em atualizar"
        
class Questao(models.Model):
    questao = models.CharField(max_length=200)
    portaria = models.CharField(max_length=4, choices=[("SV","SV"), ('OIVA', 'OIVA'),("PP", 'PP')], default="SV", null=True)
    titulo = models.CharField(max_length=200, null=True)
    numero = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.portaria) + ' - '+self.questao
    
class AnaliseProcesso(models.Model):
    semana = models.ForeignKey(Semana, on_delete=models.CASCADE)
    OS = models.IntegerField(help_text="Nº da OS", null=True)
    data = models.DateField(default=date.today)
    user = models.CharField(max_length=30, default="João")
    observacoes = models.TextField(help_text="Observações", null=True)
    realizado = models.BooleanField(default=False)
    NC = models.CharField(max_length=3, choices=[('Sim', 'Sim'),("Não","Não")], default="Não")
        
    def __str__(self):
        if self.realizado == True:
            return str(self.OS)
        else:
            return "Análise a realizar, clique em atualizar"
    
class AnaliseProcessoResposta(models.Model):
    resposta = models.CharField(max_length=200, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default='A')
    analiseProcesso = models.ForeignKey(AnaliseProcesso, on_delete=models.CASCADE,  null=True)
    quest = models.ForeignKey(Questao, on_delete=models.CASCADE, null=True, related_name='questoes')
    