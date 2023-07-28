# Generated by Django 4.1.1 on 2022-10-16 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0016_alter_itemtobuy_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtobuy',
            name='urgent',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='itemtobuy',
            name='category',
            field=models.CharField(choices=[('hygien', 'Hygien'), ('food', 'Food'), ('clothes', 'Clothes'), ('documents', 'Documents'), ('family', 'Family'), ('debt', 'Debt'), ('house', 'House'), ('cotas', 'Cotas')], default='hygien', max_length=20),
        ),
    ]