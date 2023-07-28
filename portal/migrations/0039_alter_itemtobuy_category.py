# Generated by Django 4.1.1 on 2022-12-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0038_itemtobuy_buy_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtobuy',
            name='category',
            field=models.CharField(choices=[('clothes', 'Clothes'), ('cotas', 'Cotas'), ('debt', 'Debt'), ('documents', 'Documents'), ('family', 'Family'), ('food', 'Food'), ('house', 'House'), ('hygien', 'Hygien'), ('utilities', 'Utilities')], default='hygien', max_length=20),
        ),
    ]
