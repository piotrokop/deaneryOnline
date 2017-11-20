# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
		return (self.name)


class UserRole(models.Model):
	name = models.CharField(max_length=15)

	def __str__(self):
		return self.name

#Profile and default User model are related as one to one
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	role_id = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True)
	semester = models.IntegerField(null=True)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()


#Method injection to User class
def get_full_name(self):
	return '%s %s' % (self.last_name, self.first_name)

User.add_to_class("__str__", get_full_name)

