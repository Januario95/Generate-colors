# Generated by Django 4.1.1 on 2022-10-12 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0012_itemtobuy_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtobuy',
            name='item_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
