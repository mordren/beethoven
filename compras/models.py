from django.db import models

# Create your models here.
class Compras(models.Model):
    descricao = models.CharField(max_length=60)
    reponsavelCompra = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    empresaContratada = models.CharField(max_length=50)
    responsavelAnuencia = models.CharField(max_length=50)
    integridade = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Se os mesmo estão íntegros, bem lacrados nas suas embalagens e funcionando:", null=True)
    requisitosNorma = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Se o mesmo cumpre os requisitos da norma, para qual foi comprado:", null=True)
    metodologia = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Verificar se foi usada a metodologia correta na calibração:", null=True)
    requisitos = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Verificar atendimento aos requisitos solicitados:", null=True)
    calibracao = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Verificar se o equipamento calibrado foi aprovado", null=True)
    observacoes = models.TextField(help_text="Observações", null=True)