# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-11-24 20:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0008_userdepartment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdepartment',
            options={'verbose_name': 'User Department', 'verbose_name_plural': 'User Departments'},
        ),
    ]