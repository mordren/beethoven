# Generated by Django 4.2.5 on 2023-09-25 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0014_compra_datarecebimento_alter_compra_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='dataRecebimento',
            field=models.DateField(auto_created=True),
        ),
    ]
