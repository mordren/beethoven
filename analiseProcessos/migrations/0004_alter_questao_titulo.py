# Generated by Django 4.2.5 on 2023-10-03 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analiseProcessos', '0003_analiseprocesso_questao_formulariorespondido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questao',
            name='titulo',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
