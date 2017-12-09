# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from course.models import Course
from user.models import UserCourse, UserRole, Profile
from django.contrib.auth.models import User

# Create your tests here.

class UserUserGradeTestCase(TestCase):

	def setUp(self):
		#potrzebne stworzenie urzytkowników
		pass

	def test_get_all_user_grades(self):
		assert False
		
	def test_get_all_professor_grades(self):
		assert False
		
	def test_get_grade_by_course_part(self):
		assert False
		
	def test_get_grade_by_course(self):
		assert False
