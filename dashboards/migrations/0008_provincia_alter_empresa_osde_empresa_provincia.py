# Generated by Django 4.1.9 on 2023-06-03 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0007_alter_propiedadequipo_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, verbose_name='Provincia')),
                ('codigo', models.CharField(max_length=2, verbose_name='Código')),
                ('sigla', models.CharField(max_length=3, verbose_name='Sigla')),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
                'db_table': 'provincia',
            },
        ),
        migrations.AlterField(
            model_name='empresa',
            name='osde',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboards.osde', verbose_name='Osde'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='provincia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboards.provincia', verbose_name='Provincia'),
        ),
    ]
