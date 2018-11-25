# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-11-24 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0009_auto_20181125_0202'),
        ('case', '0007_auto_20181125_0202'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultcase',
            name='user_department',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_department_for_result', to='department.UserDepartment'),
        ),
        migrations.AddField(
            model_name='solutioncase',
            name='user_department',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_department_for_solution', to='department.UserDepartment'),
        ),
    ]
