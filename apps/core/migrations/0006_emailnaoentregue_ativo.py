# Generated by Django 3.2.5 on 2021-07-20 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210720_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailnaoentregue',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]