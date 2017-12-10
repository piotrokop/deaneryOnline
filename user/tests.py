# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from django.contrib.auth.models import User
from user.models import UserRole
from user.models import UserCourse
from course.models import Course

# Create your tests here.

class UserCourseTestCase(TestCase):

	def setUp(self):
		self.course1 = Course.objects.create(
			name = 'Test1',
			description = 'Description for test1',
			exercises = None,
			laboratories = 70,
			project = 30,
			seminars = None,
			exam = 1,
			ects = 5
			)
		self.course2 = Course.objects.create(
			name = 'Test2',
			description = 'Description for test2',
			exercises = 120,
			laboratories = None,
			project = None,
			seminars = None,
			exam = 0,
			ects = 3
			)

		UserRole.objects.create(
			id = 1,
			name = 'students')

		UserRole.objects.create(
			id = 2,
			name = 'professors')

		self.student = User.objects.create_user(
			username = 'student', 
			password = 'test123', 
			first_name = 'Tom', 
			last_name = 'Brown')
		self.student.profile.semester = 5

		self.professor = User.objects.create_user(
			username = 'professor', 
			password = 'test123', 
			first_name = 'John', 
			last_name = 'Smith')
		self.professor.profile.role_id = 2

		UserCourse.objects.create(
			profile = self.student.profile,
			course = self.course1,
			accepted = True)

		UserCourse.objects.create(
			profile = self.student.profile,
			course = self.course2,
			accepted = False)
			
		UserCourse.objects.create(
			profile = self.professor.profile,
			course = self.course1,
			accepted = True)
		pass

	def test_get_role_by_name(self):
		try:
			role1 = UserRole.objects.get(name = 'students')
			role2 = UserRole.objects.get(name = 'professors')
		except:
			self.assertTrue(False)
		else:
			self.assertTrue(True)

	def test_get_user_by_username(self):
		try:
			user1 = User.objects.get(username = 'student')
			user2 = User.objects.get(username = 'professor')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(user1, self.student)
			self.assertEqual(user2, self.professor)

	def test_get_non_existing_user(self):
		try:
			test = Course.objects.get(username = 'user')
		except:
			pass
		else:
			self.assertTrue(False)

	def test_get_all_user_courses(self):
		try:
			students_courses = UserCourse.objects.filter(profile = self.student.profile)
			professors_courses = UserCourse.objects.filter(profile = self.professor.profile)
		except:
			self.assertTrue(False)
		else:
			courses = []
			for user_course in students_courses:
				courses.append(user_course.course)

			self.assertEqual(len(students_courses), 2)
			self.assertTrue(self.course1 in courses)
			self.assertTrue(self.course2 in courses)

			courses = []
			for user_course in professors_courses:
				courses.append(user_course.course)

			self.assertEqual(len(professors_courses), 1)
			self.assertTrue(self.course1 in courses)

		
	def test_get_course_from_user_courses(self):
		try:
			students_course = UserCourse.objects.get(profile = self.student.profile, course = self.course1)
			professors_course = UserCourse.objects.get(profile = self.professor.profile, course = self.course1)
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(students_course.profile, self.student.profile)
			self.assertEqual(students_course.course, self.course1)

			self.assertEqual(professors_course.profile, self.professor.profile)
			self.assertEqual(professors_course.course, self.course1)

