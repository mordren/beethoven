# Generated by Django 4.2.5 on 2023-10-02 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analiseProcessos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analiseprocessosv',
            name='portaria',
        ),
    ]
