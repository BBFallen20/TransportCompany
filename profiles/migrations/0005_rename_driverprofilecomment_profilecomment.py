# Generated by Django 3.2.5 on 2021-07-30 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profiles', '0004_rename_driver_profile_id_driverprofilecomment_profile_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DriverProfileComment',
            new_name='ProfileComment',
        ),
    ]