# Generated by Django 4.1.9 on 2023-06-07 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0015_alter_organismo_fecha_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriaequipo',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='categoriainsumo',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='categoriaparte',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='categoriapieza',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='marca',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='marcamodelo',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='modelo',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='organismo',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='osde',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='parte',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='pieza',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='propiedad',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='propiedadequipo',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='propiedadinsumo',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='propiedadparte',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='propiedadpieza',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='provincia',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
