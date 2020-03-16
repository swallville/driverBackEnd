# Generated by Django 3.0.4 on 2020-03-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truck_type', models.CharField(choices=[('1', 'Caminhão 3/4'), ('2', 'Caminhão Toco'), ('3', 'Caminhão Truck'), ('4', 'Carreta Simples'), ('5', 'Carreta Eixo Extendido')], max_length=2, verbose_name='Truck Type')),
            ],
            options={
                'verbose_name': 'Truck',
                'verbose_name_plural': 'Trucks',
                'ordering': ['id'],
                'permissions': (('detail_truck', 'Can detail Truck'), ('list_truck', 'Can list Truck')),
            },
        ),
    ]
