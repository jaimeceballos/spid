# Generated by Django 2.0.2 on 2019-01-30 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preventivos', '0004_remove_fields_fecha_desde_hasta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='domicilios',
            old_name='fecha_desde_temp',
            new_name='fecha_desde',
        ),
        migrations.RenameField(
            model_name='domicilios',
            old_name='fecha_hasta_temp',
            new_name='fecha_hasta',
        ),
    ]
