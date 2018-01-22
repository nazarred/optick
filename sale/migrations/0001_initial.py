# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-22 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SoldGlasses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kod', models.CharField(max_length=15)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('price_opt', models.FloatField()),
                ('price_roz', models.IntegerField()),
                ('dpt', models.FloatField(blank=True, null=True)),
                ('pcs', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('sale_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
