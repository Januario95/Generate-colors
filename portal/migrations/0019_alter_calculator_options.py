# Generated by Django 4.1.1 on 2022-10-26 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0018_calculator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calculator',
            options={'verbose_name': 'Calculation', 'verbose_name_plural': 'Calculations'},
        ),
    ]
