# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_auto_20170322_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='equipment_needed',
            field=models.CharField(choices=[('Basic Gym Equipment', 'Minimal'), ('Extensive Gym Equipment', 'Extensive')], max_length=30),
        ),
        migrations.AlterField(
            model_name='routine',
            name='routine_type',
            field=models.CharField(choices=[('Strength', 'Strength'), ('Hypertrophy', 'Hypertrophy')], max_length=30),
        ),
    ]
