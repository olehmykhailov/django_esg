# Generated by Django 5.2.1 on 2025-06-01 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etl_app', '0005_alter_energydata_value_alter_greenhousedata_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='metadata',
            name='ticker',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
