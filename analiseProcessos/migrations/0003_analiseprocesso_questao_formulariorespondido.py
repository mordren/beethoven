# Generated by Django 4.2.5 on 2023-10-03 13:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analiseProcessos', '0002_remove_analiseprocessosv_portaria'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnaliseProcesso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OS', models.IntegerField(help_text='Nº da OS', null=True)),
                ('data', models.DateField(default=datetime.date.today)),
                ('user', models.CharField(default='João', max_length=30)),
                ('portaria', models.CharField(choices=[('SV', 'SV'), ('OIVA', 'OIVA'), ('PP', 'PP')], default='SV', max_length=4, null=True)),
                ('observacoes', models.TextField(help_text='Observações', null=True)),
                ('realizado', models.BooleanField(default=False)),
                ('NC', models.CharField(choices=[('Sim', 'Sim'), ('Não', 'Não')], default='Não', max_length=3)),
                ('semana', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analiseProcessos.semana')),
            ],
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questao', models.CharField(max_length=200)),
                ('portaria', models.CharField(choices=[('SV', 'SV'), ('OIVA', 'OIVA'), ('PP', 'PP')], default='SV', max_length=4, null=True)),
                ('titulo', models.CharField(max_length=30, null=True)),
                ('numero', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FormularioRespondido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta', models.CharField(choices=[('A', 'A'), ('R', 'R'), ('NA', 'NA')], default='A', max_length=200)),
                ('analiseProcesso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='analiseProcessos.analiseprocesso')),
                ('quest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questoes', to='analiseProcessos.questao')),
            ],
        ),
    ]