# Generated by Django 4.1.1 on 2022-10-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0031_alter_color_blue_alter_color_green_alter_color_red'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='blue',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='color',
            name='green',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='color',
            name='red',
            field=models.IntegerField(),
        ),
    ]
