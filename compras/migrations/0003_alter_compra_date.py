# Generated by Django 4.2.5 on 2023-10-03 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0002_alter_compra_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='date',
            field=models.DateField(null=True, verbose_name=datetime.datetime(2023, 10, 3, 13, 47, 26, 295215, tzinfo=datetime.timezone.utc)),
        ),
    ]
