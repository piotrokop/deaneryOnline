# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Course(models.Model):
	course_id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length=30)

	class Meta:
		ordering = ['name']
	
	def __str__(self):
		return (self.name)