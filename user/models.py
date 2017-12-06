# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserRole(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name
		
		
		
		

#Profile and default User model are related as one to one
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField('course.Course', through='user.UserCourse')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, default=1)
    semester = models.IntegerField(null=True)		
	
class UserCourse(models.Model):
    profile = models.ForeignKey(Profile)
    course = models.ForeignKey('course.Course')
    accepted = models.BooleanField()

    class Meta:
        unique_together = ('profile', 'course',)     	
	
	
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()	