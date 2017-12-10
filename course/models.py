# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from app.models import Profile, Course
from user.models import Profile

# Create your models here.
        
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    exercises = models.IntegerField(null=True, default=None, blank=True)
    laboratories = models.IntegerField(null=True, default=None, blank=True)
    project = models.IntegerField(null=True, default=None, blank=True)
    seminars = models.IntegerField(null=True, default=None, blank=True)
    exam = models.IntegerField(null=True, default=None, blank=True)
    ects = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name             
