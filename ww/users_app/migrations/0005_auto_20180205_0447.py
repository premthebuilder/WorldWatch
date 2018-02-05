# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-05 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0004_auto_20180205_0211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='gps_location',
        ),
        migrations.AddField(
            model_name='location',
            name='latitude',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='location',
            name='longitude',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
