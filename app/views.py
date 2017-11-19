# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import Course
from app.forms import CourseForm

# Create your views here.
def create_course(request):
	if request.method == "POST":
		form = CourseForm(request.POST)
		course = form.save(commit=False)
		if request.POST.get('if_exer'):
			course.exercises = request.POST.get['exercises']
		else:
			course.exercises = 0
		if request.POST.get('if_lab'):
			course.laboratories = request.POST.get('laboratories') 
		else:
			course.laboratories = 0
		if request.POST.get('if_proj'):
			course.project = request.POST.get('project')
		else:
			course.project = 0
		if request.POST.get('if_sem'):
			course.seminars = request.POST.get('seminars')
		else:
			course.seminars = 0
		if request.POST.get('exam'):
			course.exam = 1
		else:
			course.exam = 0
		course.save()
		return render(request, 'course/courses.html')
	else:
		form = CourseForm()
	return render(request, 'course/create-course.html', {"form" : form})
	
	
	
def edit_course(request, id):
	course = Course.objects.get(course_id = id)
	inexam = True if course.exam==1 else False
	inexer = course.exercises if course.exercises > 0 else ''
	inlab = course.laboratories if course.laboratories > 0 else ''
	inproj = course.project if course.project > 0 else ''
	insem = course.seminars if course.seminars > 0 else ''
	
	ifexer = True if course.exercises > 0 else False
	iflab = True if course.laboratories > 0 else False
	ifproj = True if course.project > 0 else False
	ifsem = True if course.seminars > 0 else False
	
	init = {'exam': inexam ,
		'exercises': inexer,
		'laboratories': inlab,
		'project':inproj,
		'seminars':insem,
		'if_exer':ifexer,
		'if_lab':iflab,
		'if_proj':ifproj,
		'if_sem':ifsem}
	if request.method == "POST":
		form = CourseForm(request.POST, instance = course, initial = init)
			
		if form.is_valid():
			course = form.save(commit=False)
			if request.POST.get('if_exer'):
				course.exercises = request.POST.get['exercises']
			else:
				course.exercises = 0
			if request.POST.get('if_lab'):
				course.laboratories = request.POST.get('laboratories') 
			else:
				course.laboratories = 0
			if request.POST.get('if_proj'):
				course.project = request.POST.get('project')
			else:
				course.project = 0
			if request.POST.get('if_sem'):
				course.seminars = request.POST.get('seminars')
			else:
				course.seminars = 0
			if request.POST.get('exam'):
				course.exam = 1
			else:
				course.exam = 0
			course.save()
			return render(request, 'course/courses.html')
	else:
		form = CourseForm(instance=course, initial = init)
			
	return render(request, 'course/create-course.html', {"form" : form, "edit": 1})

def courses(request):
	user_role = 2
	courses = Course.objects.all()
	return render(request, 'course/courses.html', {"role" : user_role, "all_courses" : courses})

@login_required()
def createview(request):
	return render(request, 'main.html')