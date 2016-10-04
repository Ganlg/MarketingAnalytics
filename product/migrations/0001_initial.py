# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-03 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.PositiveIntegerField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250, null=True)),
            ],
        ),
    ]