# Generated by Django 3.2.5 on 2021-07-08 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210707_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='filial',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.filial'),
            preserve_default=False,
        ),
    ]
