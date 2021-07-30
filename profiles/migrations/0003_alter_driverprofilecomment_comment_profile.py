# Generated by Django 3.2.5 on 2021-07-30 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profiles', '0002_driverprofilecomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverprofilecomment',
            name='comment_profile',
            field=models.ForeignKey(limit_choices_to=models.Q(('app_label', 'profiles'), ('model', 'driverprofile')), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
