# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 20:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20171121_2144'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usercourse',
            unique_together=set([('user', 'course')]),
        ),
    ]