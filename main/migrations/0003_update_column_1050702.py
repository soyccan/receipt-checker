# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 01:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('main', '0002_set_prize'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prize',
            old_name='type',
            new_name='typeid',
        ),
        migrations.RenameField(
            model_name='winnum',
            old_name='date',
            new_name='datecode',
        ),
        migrations.RenameField(
            model_name='winnum',
            old_name='type',
            new_name='prizetype',
        ),
    ]
