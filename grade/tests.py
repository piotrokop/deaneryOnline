# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from course.models import Course
from user.models import UserCourse, UserRole, Profile
from django.contrib.auth.models import User
from grade.models import UserGrade
from sets import Set

# Create your tests here.

class UserGradeTestCase(TestCase):

	def setUp(self):
		self.course1 = Course.objects.create(
			name = 'Test1',
			description = 'Description for test1',
			laboratories = 70,
			project = 30,
			exam = 1,
			ects = 5
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
		
		self.student2 = User.objects.create_user(
			username = 'student2', 
			password = 'test123', 
			first_name = 'Tommas', 
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
			profile = self.student2.profile,
			course = self.course1,
			accepted = True)
			
		UserCourse.objects.create(
			profile = self.professor.profile,
			course = self.course1,
			accepted = True)
			
		UserGrade.objects.create(
			grade = 4.5,
			is_final = True,
			course = self.course1,
			category = 'project',
			professor_user = self.professor.profile,
			student_user = self.student.profile)
		
		UserGrade.objects.create(
			grade = 3.0,
			is_final = True,
			course = self.course1,
			category = 'exam',
			professor_user = self.professor.profile,
			student_user = self.student.profile)
		
		UserGrade.objects.create(
			grade = 5.0,
			is_final = True,
			course = self.course1,
			category = 'exam',
			professor_user = self.professor.profile,
			student_user = self.student2.profile)		

	def internal_posession_function(self,grades):
		course_set = Set()
		courses = []
		grade_set = (grade for grade in grades )
		for grade in grade_set:
			course_set.add(grade.course)
		for c in course_set:
			course = Course.objects.get(course_id=c.course_id)
			courses.append({'Name' : course.name ,'Id' : course.course_id , 'ECTS' : course.ects, 'Pos' : len(courses)})
		for grade in grades:
			for c in courses:
				if c['Id']==grade.course_id:
					courses[c['Pos']][grade.category]=grade.grade
		return courses
			
	def test_get_all_user_grades(self):
		grades = UserGrade.objects.filter(student_user_id=self.student.id, is_final=True)
		courses = self.internal_posession_function(grades)		
		self.assertAlmostEqual(courses[0]['project'], 4.5)
		self.assertAlmostEqual(courses[0]['exam'], 3.0)
		
	def test_get_all_professor_grades(self):
		grades = UserGrade.objects.filter(professor_user_id=self.professor.id, is_final=True)			
		self.assertEqual(len(grades), 3)
		course_part_set = Set()
		for grade in grades:
			course_part_set.add(grade.category)
		self.assertEqual(len(course_part_set), 2)
		
	def test_get_grade_by_course_part(self):
		grades = UserGrade.objects.filter(is_final=True, course=self.course1, category='exam')
		self.assertEqual(len(grades), 2)
		grades = UserGrade.objects.filter(is_final=True, course=self.course1, category='project')
		self.assertEqual(len(grades), 1)
		
	def test_get_grade_by_course(self):
		grades = UserGrade.objects.filter(course_id=self.course1)
		self.assertEqual(len(grades), 3)
