# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-06 16:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Category'),
        ),
    ]
