from django.db import models
from datetime import date
from user.models import UserProfile
from django.utils import timezone
# Create your models here.
class Compra(models.Model):
    responsavelCompra = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    descricao = models.CharField(max_length=60)    
    date = models.DateField(timezone.now(), null=True)
    empresaContratada = models.CharField(max_length=50)
    responsavelAnuencia = models.CharField(max_length=50)
    integridade = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Se os mesmo estão íntegros, bem lacrados nas suas embalagens e funcionando:", null=True)
    requisitosNorma = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Se o mesmo cumpre os requisitos da norma, para qual foi comprado:", null=True)
    labRBC = models.CharField(verbose_name="Laboratório RBC", max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Verificar se o certificado foi feito por laboratório da RBC:", null=True)
    metodologia = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Verificar se foi usada a metodologia correta na calibração:", null=True)
    requisitos = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Verificar atendimento aos requisitos solicitados:", null=True)
    calibracao = models.CharField(max_length=20, choices=[('A','A'),('R', 'R'),('NA', 'NA')], default="A", help_text="Verificar se o equipamento calibrado foi aprovado", null=True)
    observacoes = models.TextField(help_text="Observações", null=True)
    dataRecebimento = models.DateField(auto_created=True, null=True)
        
    def __str__(self):
        return self.descricao + ' - ' + self.date.strftime("%d/%m/%y")
    
    class Meta:
        ordering = ['-date']