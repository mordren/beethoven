# Generated by Django 4.2.5 on 2023-09-24 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_userprofile_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.empresa'),
        ),
    ]
