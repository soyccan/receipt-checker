# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('type', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WinNum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('date', models.TextField()),
                ('number', models.TextField()),
                ('type', models.ForeignKey(to='main.Prize')),
            ],
        ),
    ]
