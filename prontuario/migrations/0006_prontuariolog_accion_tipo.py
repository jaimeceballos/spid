# Generated by Django 2.0.2 on 2019-01-21 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prontuario', '0005_entidad_id_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='prontuariolog',
            name='accion_tipo',
            field=models.CharField(blank=True, default=None, max_length=3, null=True),
        ),
    ]
