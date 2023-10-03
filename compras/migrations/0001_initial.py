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
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataRecebimento', models.DateField(auto_created=True, null=True)),
                ('descricao', models.CharField(max_length=60)),
                ('date', models.DateField(null=True, verbose_name=datetime.datetime(2023, 10, 2, 19, 20, 42, 509429, tzinfo=datetime.timezone.utc))),
                ('empresaContratada', models.CharField(max_length=50)),
                ('responsavelAnuencia', models.CharField(max_length=50)),
                ('integridade', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='Se os mesmo estão íntegros, bem lacrados nas suas embalagens e funcionando:', max_length=20, null=True)),
                ('requisitosNorma', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='Se o mesmo cumpre os requisitos da norma, para qual foi comprado:', max_length=20, null=True)),
                ('labRBC', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='Verificar se o certificado foi feito por laboratório da RBC:', max_length=20, null=True, verbose_name='Laboratório RBC')),
                ('metodologia', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='Verificar se foi usada a metodologia correta na calibração:', max_length=20, null=True)),
                ('requisitos', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='Verificar atendimento aos requisitos solicitados:', max_length=20, null=True)),
                ('calibracao', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', help_text='Verificar se o equipamento calibrado foi aprovado', max_length=20, null=True)),
                ('observacoes', models.TextField(help_text='Observações', null=True)),
                ('responsavelCompra', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.userprofile')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
