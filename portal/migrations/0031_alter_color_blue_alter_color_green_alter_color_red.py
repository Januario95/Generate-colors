# Generated by Django 4.1.1 on 2022-10-30 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0030_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='blue',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='color',
            name='green',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='color',
            name='red',
            field=models.CharField(max_length=256),
        ),
    ]
