# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-04-08 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeside_server', '0023_auto_20190219_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='pid',
            field=models.CharField(blank=True, max_length=128, unique=True, verbose_name='pid'),
        ),
    ]
