# Generated by Django 4.2.5 on 2023-10-02 19:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='date',
            field=models.DateField(null=True, verbose_name=datetime.datetime(2023, 10, 2, 19, 26, 49, 715064, tzinfo=datetime.timezone.utc)),
        ),
    ]