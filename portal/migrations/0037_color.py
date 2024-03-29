# Generated by Django 4.1.1 on 2022-10-30 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0036_delete_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('red', models.IntegerField()),
                ('green', models.IntegerField()),
                ('blue', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
