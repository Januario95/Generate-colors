# Generated by Django 4.1.1 on 2022-10-26 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0019_alter_calculator_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculator',
            name='first_number',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='calculator',
            name='second_number',
            field=models.FloatField(),
        ),
    ]
