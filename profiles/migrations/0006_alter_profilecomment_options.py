# Generated by Django 3.2.5 on 2021-08-02 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_rename_driverprofilecomment_profilecomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profilecomment',
            options={'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
    ]
