# Generated by Django 3.2.5 on 2021-07-30 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverProfileComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_profile_id', models.PositiveIntegerField()),
                ('content', models.TextField(max_length=1500, verbose_name='Comment text')),
                ('muted', models.BooleanField(default=False, verbose_name='Comment mute flag')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Comment user')),
                ('comment_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.driverprofilecomment', verbose_name='Parent comment')),
            ],
        ),
    ]
