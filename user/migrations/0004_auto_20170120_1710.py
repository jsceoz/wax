# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-20 09:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20170120_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dormitory',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='user.Dormitory'),
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='user.School'),
        ),
    ]
