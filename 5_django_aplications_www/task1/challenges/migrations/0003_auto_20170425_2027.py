# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 20:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_challenge_days_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenge',
            old_name='days_done',
            new_name='counter',
        ),
    ]
