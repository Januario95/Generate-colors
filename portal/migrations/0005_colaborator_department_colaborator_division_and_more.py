# Generated by Django 4.1.1 on 2022-09-30 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborator',
            name='department',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='colaborator',
            name='division',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='colaborator',
            name='job_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='colaborator',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]
