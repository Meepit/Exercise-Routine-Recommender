# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0006_auto_20170323_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='equipment_needed',
            field=models.IntegerField(choices=[('0', 'Basic Gym Equipment'), ('1', 'Extensive Gym Equipment')]),
        ),
        migrations.AlterField(
            model_name='routine',
            name='routine_type',
            field=models.IntegerField(choices=[('0', 'Strength'), ('1', 'Hypertrophy')]),
        ),
    ]
