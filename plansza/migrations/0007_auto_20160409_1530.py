# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-09 15:30
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('plansza', '0006_auto_20160409_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 9, 15, 29, 56, 860342, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 9, 15, 30, 4, 8492, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventhour',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='hours', to=settings.AUTH_USER_MODEL),
        ),
    ]
