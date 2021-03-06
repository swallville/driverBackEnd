# Generated by Django 3.0.4 on 2020-03-13 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='has_vehicle',
            field=models.BooleanField(verbose_name='Driver has vehicle?'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='is_active',
            field=models.BooleanField(verbose_name='Is active?'),
        ),
        migrations.AlterField(
            model_name='register',
            name='is_Loaded',
            field=models.BooleanField(verbose_name='Is loaded?'),
        ),
    ]
