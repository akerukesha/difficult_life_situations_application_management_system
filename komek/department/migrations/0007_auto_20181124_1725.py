# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-11-24 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0006_auto_20181124_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='timestamp',
            field=models.BigIntegerField(default=0, verbose_name='Department timestamp'),
        ),
    ]