# Generated by Django 4.1.9 on 2023-05-27 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empresa',
            name='municipio',
        ),
    ]
