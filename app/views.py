# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import formset_factory
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.forms import SignUpForm, ManageCourseForm
from app.models import UserRole, Profile
from django.contrib.auth.models import User
from app.helper import Values, DBHelper
from sets import Set
from app.models import UserGrade
from course.forms import CourseForm
from .models import UserCourse
		
def grades(request):
	if request.user.is_authenticated():
		user = DBHelper.get_user(request)
		grades = UserGrade.objects.filter(student_user_id=user, is_final=True)
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
		return render(request, 'course/grades.html', {
            "role_obj": user.role,
            "gradeList" : courses
        })

@login_required()
def createview(request):
    user = DBHelper.get_user(request)
    return render(request, 'main.html', {"role_obj": user.role})
	
	
def course_manage(request, id):
    course = Course.objects.get(course_id = id)
    user_courses = UserCourse.objects.filter(course=course, accepted=1)
    ManageCourseFormSet = formset_factory(ManageCourseForm, extra = user_courses.count())
    zipped = []
    users_list = [(user_course.profile.user.first_name, user_course.profile.user.last_name) for user_course in user_courses]
    if request.method == 'POST':
        formset = ManageCourseFormSet(request.POST)
        if formset.is_valid():
            user_index = 0
            for form in formset:
                data = form.cleaned_data
                zipped.append((form, users_list[user_index]))
                for field in form:
                    if data[field.name] != 'None' and data[field.name] != '':
                        if field.name == 'final_grade':
                            usergrade, created = UserGrade.objects.get_or_create(category=field.name,student_user_id=user_courses[user_index].profile.user_id, course_id=id, defaults={'grade': 3.0, 'is_final': False, 'professor_user_id': request.user.id})
                            if created:
                                usergrade.grade = data[field.name]
                                usergrade.is_final = True
                                usergrade.course_id = id
                                usergrade.category = field.name
                                usergrade.professor_user_id = request.user.id
                                usergrade.student_user_id = user_courses[user_index].profile.user_id
                                usergrade.save()
                            else:
                                usergrade.grade = data[field.name]
                                usergrade.save()
                        elif getattr(course, field.name) > 0:
                            usergrade, created = UserGrade.objects.get_or_create(category=field.name,student_user_id=user_courses[user_index].profile.user_id, course_id=id, defaults={'grade': 3.0, 'is_final': False, 'professor_user_id': request.user.id})
                            if created:
                                usergrade.grade = data[field.name]
                                usergrade.is_final = True
                                usergrade.course_id = id
                                usergrade.category = field.name
                                usergrade.professor_user_id = request.user.id
                                usergrade.student_user_id = user_courses[user_index].profile.user_id
                                usergrade.save()
                            else:
                                usergrade.grade = data[field.name]
                                usergrade.save()
                user_index += 1
    else:
        user_index = 0
        formset = ManageCourseFormSet()
        for form in formset:
            zipped.append((form, users_list[user_index]))
            user_index += 1

    user = DBHelper.get_user(request)
    return render(request, 'course/course-manage.html', {"role_obj": user.role, "course": course, "zipped": zipped, "formset": formset, "user_courses": user_courses})


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.role = UserRole.objects.get(id=form.cleaned_data.get('role'))
			user.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('/accounts/login/')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})