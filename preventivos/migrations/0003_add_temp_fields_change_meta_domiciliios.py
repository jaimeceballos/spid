# Generated by Django 2.0.2 on 2019-01-30 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preventivos', '0002_cambio_clave_unica_ciudad'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='domicilios',
            options={'get_latest_by': 'id'},
        ),
        migrations.AddField(
            model_name='domicilios',
            name='fecha_desde_temp',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='domicilios',
            name='fecha_hasta_temp',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterUniqueTogether(
            name='domicilios',
            unique_together={('personas', 'ref_ciudades', 'barrio_codigo', 'calle', 'altura')},
        ),
    ]
