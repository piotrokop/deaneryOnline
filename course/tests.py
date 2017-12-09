# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from course.models import Course

# Create your tests here.

class CourseTestCase(TestCase):

	def setUp(self):
		Course.objects.create(
			name = 'Test1',
			description = 'Description for test1',
			exercises = None,
			laboratories = 70,
			project = 30,
			seminars = None,
			exam = 1,
			ects = 5
			)
		Course.objects.create(
			name = 'Test2',
			description = 'Description for test2',
			exercises = 120,
			laboratories = None,
			project = None,
			seminars = None,
			exam = 0,
			ects = 3
			)

	def test_get_course_from_base(self):
		try:
			test1 = Course.objects.get(name = 'Test1')
			test2 = Course.objects.get(name = 'Test2')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(test1.name, 'Test1')
			self.assertEqual(test2.name, 'Test2')
	
	def test_get_non_existing_course(self):
		try:
			test = Course.objects.get(name = 'Test3')
		except:
			pass
		else:
			self.assertTrue(False)
		
	def test_get_descriptions(self):
		try:
			test1 = Course.objects.get(name = 'Test1')
			test2 = Course.objects.get(name = 'Test2')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(test1.description, 'Description for test1')
			self.assertEqual(test2.description, 'Description for test2')
			
	def test_get_exercises(self):
		try:
			test1 = Course.objects.get(name = 'Test1')
			test2 = Course.objects.get(name = 'Test2')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(test1.exercises, None)
			self.assertEqual(test2.exercises, 120)
			
	def test_get_laboratories(self):
		try:
			test1 = Course.objects.get(name = 'Test1')
			test2 = Course.objects.get(name = 'Test2')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(test1.laboratories, 70)
			self.assertEqual(test2.laboratories, None)
	
	def test_get_project(self):
		try:
			test1 = Course.objects.get(name = 'Test1')
			test2 = Course.objects.get(name = 'Test2')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(test1.project, 30)
			self.assertEqual(test2.project, None)
				
	def test_get_seminars(self):
		try:
			test1 = Course.objects.get(name = 'Test1')
			test2 = Course.objects.get(name = 'Test2')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(test1.seminars, None)
			self.assertEqual(test2.seminars, None)
			
	def test_get_exam(self):
		try:
			test1 = Course.objects.get(name = 'Test1')
			test2 = Course.objects.get(name = 'Test2')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(test1.exam, 1)
			self.assertEqual(test2.exam, 0)
			
	def test_get_exam_nother_method(self):
		try:
			test1 = Course.objects.get(name = 'Test1')
			test2 = Course.objects.get(name = 'Test2')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(test1.exam, True)
			self.assertEqual(test2.exam, False)
		
	def test_get_ects(self):
		try:
			test1 = Course.objects.get(name = 'Test1')
			test2 = Course.objects.get(name = 'Test2')
		except:
			self.assertTrue(False)
		else:
			self.assertEqual(test1.ects, 5)
			self.assertEqual(test2.ects, 3)	
		
		