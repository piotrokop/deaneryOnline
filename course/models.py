# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from app.models import Profile, Course

# Create your models here.
        
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    exercises = models.IntegerField(null=True)
    laboratories = models.IntegerField(null=True)
    project = models.IntegerField(null=True)
    seminars = models.IntegerField(null=True)
    exam = models.IntegerField(null=True)
    ects = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name        
        
        
