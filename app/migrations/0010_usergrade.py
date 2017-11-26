# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20171126_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGrade',
            fields=[
                ('usergrade', models.AutoField(primary_key=True, serialize=False)),
                ('grade', models.DecimalField(decimal_places=1, max_digits=2)),
                ('is_final', models.BooleanField()),
                ('category', models.CharField(max_length=30)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
                ('professor_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professor', to='app.Profile')),
                ('student_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='app.Profile')),
            ],
        ),
    ]
