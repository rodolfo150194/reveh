# Generated by Django 4.1.9 on 2023-05-29 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0005_categoriaequipo_categoriainsumo_categoriaparte_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='chapa',
            field=models.CharField(max_length=50, null=True, verbose_name='Chapa'),
        ),
    ]
