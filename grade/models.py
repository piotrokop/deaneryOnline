# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Profile


class UserGrade(models.Model):
	usergrade_id = models.AutoField(primary_key=True)
	grade = models.DecimalField(max_digits=2, decimal_places=1)
	is_final = models.BooleanField()
	course = models.ForeignKey('course.Course')
	category = models.CharField(max_length=30)
	professor_user = models.ForeignKey(Profile, related_name="professor")
	student_user = models.ForeignKey(Profile, related_name="student")
