# Generated by Django 4.2.5 on 2023-10-02 19:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateField()),
                ('fim', models.DateField()),
                ('numero', models.IntegerField()),
                ('processos', models.IntegerField(default=0)),
                ('analises', models.IntegerField(default=0)),
                ('realizado', models.BooleanField(default=False)),
                ('data', models.DateField(default=datetime.date.today)),
                ('numeroNC', models.IntegerField(default=0)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='AnaliseProcessoSV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OS', models.IntegerField(help_text='Nº da OS', null=True)),
                ('data', models.DateField(default=datetime.date.today)),
                ('user', models.CharField(default='João', max_length=30)),
                ('portaria', models.CharField(choices=[('SV', 'SV'), ('OIVA', 'OIVA'), ('PP', 'PP')], default='SV', max_length=4, null=True)),
                ('crlv', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='1)\tCRLV ou CRV ou NF compra veículo – HABILITAÇÃO do condutor', max_length=20, null=True)),
                ('decalque', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='2)\tDECALQUE do número do chassi;', max_length=2, null=True)),
                ('vistoriaInicial', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='3)\tFOR ADM 31 ORDEM DE SERVIÇO com a VISTORIA INICIAL;', max_length=2, null=True)),
                ('verificaoEscopo', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='4)\tLista de verificação correta ao escopo, rastreável, com anotações corretas, correções conforme procedimento, com quantificáveis rastreado ao equipamento entre outros;', max_length=2, null=True)),
                ('linhaInspecao', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text="5)\tRelatório da LINHA DE INSPEÇÃO, assinado por todos, 'A', com número de patrimônio, rastreavel ao veículo, equipamento calibrado entre outros;", max_length=2, null=True)),
                ('opacidade', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text="6)\tRelatório de OPACIDADE, ANÁLISE DE GASES quando aplicável, assinado por todos, 'A', com número de patrimônio, rastreavel ao veículo, equipamento calibrado entre outros;", max_length=2, null=True)),
                ('ruido', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text="7)\tRelatório de RUÍDO, quando aplicável, assinado por todos, 'A', com número de patrimônio, rastreavel ao veículo, equipamento calibrado entre outros;", max_length=2, null=True)),
                ('naoConformidade', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='8)\tRegistro de NÃO CONFORMIDADE;', max_length=2, null=True)),
                ('rasurasProcessos', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='9)\tVerificar a existência de RASURAS NOS PROCESSOS;', max_length=2, null=True)),
                ('registrosFotograficos', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='10)\tRegistro fotográfico do EIXO (s) DIANTEIRO (s) e EIXO (s) TRASEIRO (s) do veículo e a banda de rodagem dos pneus dianteiros e pneus traseiros. A foto do eixo dianteiro deve ser tirada no sentido do eixo traseiro, a foto do eixo traseiro deve ser tirada no sentido do eixo dianteiro, quando houver um terceiro eixo, o registro fotográfico deve ser tirado no sentido do eixo traseiro; Registro fotográfico do Para todos os veículos com PARA-CHOQUE homologados, um (1) registro fotográfico da plaqueta de homologação do pára-choque; Registro fotográfico do transversal do PINO-REI e de sua MESA LIMPOS ou QUINTA RODA, quando aplicável; Registro fotográfico das LATERAIS DOS VEÍCULOS com as FAIXAS REFLETIVAS, quando aplicáveis; Registro fotográfico ALÍVIO DE PESO no eixo direcional em veículos pesados, quando aplicável; Registro fotográfico da TRASEIRA DO VEÍCULO na linha de inspeção mecanizada, que tenha possibilidade de leitura da PLACA de licença no RELATÓRIO DE INSPEÇÃO.Obs. Os registros fotográficos devem conter data e hora.', max_length=2, null=True)),
                ('filmagem', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='11)\tFilmagem de todas as etapas de inspeção, verificar calibragem de pneus, ensaio de regloscopio, verificação do sistema de sinalização, ensaio de opacidade e ruído, dentre outros, a filmagem deve conter data e horas no formato (DD/MM/AAAA) e (hh:mm:ss).', max_length=2, null=True)),
                ('observacoes', models.TextField(help_text='Observações', null=True)),
                ('realizado', models.BooleanField(default=False)),
                ('NC', models.CharField(choices=[('Sim', 'Sim'), ('Não', 'Não')], default='Não', max_length=3)),
                ('semana', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analiseProcessos.semana')),
            ],
        ),
    ]
