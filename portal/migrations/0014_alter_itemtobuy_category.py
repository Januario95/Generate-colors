# Generated by Django 4.1.1 on 2022-10-12 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_alter_itemtobuy_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtobuy',
            name='category',
            field=models.CharField(choices=[('hygien', 'Hygien'), ('food', 'Food'), ('clothes', 'Clothes'), ('documents', 'Documents'), ('family', 'Family'), ('debt', 'Debt')], default='hygien', max_length=20),
        ),
    ]