# Generated by Django 3.2.5 on 2021-07-20 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_perfil_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]