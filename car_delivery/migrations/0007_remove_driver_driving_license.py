# Generated by Django 3.2.5 on 2021-07-29 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car_delivery', '0006_auto_20210729_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='driving_license',
        ),
    ]
