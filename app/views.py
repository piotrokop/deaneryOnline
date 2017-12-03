# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import formset_factory
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import Course, UserCourse, UserGrade
from app.forms import CourseForm, SignUpForm, ManageCourseForm
from app.models import UserRole, Profile
from django.contrib.auth.models import User
from app.helper import Values, DBHelper
from sets import Set

# Create your views here.
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        course = form.save(commit=False)
        if request.POST.get('if_exer'):
            course.exercises = request.POST.get('exercises')
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
        return redirect(courses);
    else:
        form = CourseForm()
    user = DBHelper.get_user(request)    
    return render(request, 'course/create-course.html', {"role_obj": user.role, "form" : form})

def edit_course(request, id):
    course = Course.objects.get(course_id=id)
    inexam = True if course.exam == 1 else False
    inexer = course.exercises if course.exercises > 0 else ''
    inlab = course.laboratories if course.laboratories > 0 else ''
    inproj = course.project if course.project > 0 else ''
    insem = course.seminars if course.seminars > 0 else ''

    ifexer = True if course.exercises > 0 else False
    iflab = True if course.laboratories > 0 else False
    ifproj = True if course.project > 0 else False
    ifsem = True if course.seminars > 0 else False

    init = {
        'exam': inexam,
        'exercises': inexer,
        'laboratories': inlab,
        'project':inproj,
        'seminars':insem,
        'if_exer':ifexer,
        'if_lab':iflab,
        'if_proj':ifproj,
        'if_sem':ifsem
    }

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course, initial=init)

        if form.is_valid():
			if request.POST.get('del_btn'):
				object = Course.objects.get(course_id=id)
				object.delete()
				return redirect(courses)
			else:
				course = form.save(commit=False)
				if request.POST.get('if_exer'):
					course.exercises = request.POST.get('exercises')
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
				return redirect(courses)
    else:
        form = CourseForm(instance=course, initial=init)

    user = DBHelper.get_user(request)
    return render(request, 'course/create-course.html', {"role_obj": user.role, "form" : form, "edit": 1})

def courses(request):
    if request.user.is_authenticated():
        user_role = DBHelper.get_user_role(request)
        user = DBHelper.get_user(request)
        user_courses = UserCourse.objects.filter(profile=user)
        rest_courses = Course.objects.exclude(course_id__in=[c.course_id for c in user_courses])

        user = DBHelper.get_user(request)
        return render(request, 'course/courses.html', {
            "role_obj": user.role,
            "role" : user_role,
            "rest_courses" : rest_courses,
            "user_courses" : user_courses
        })
		
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
		
def course_details(request, id):
    course = Course.objects.get(course_id=id)
    name = course.name
    description = course.description
    ects = course.ects
    exam = course.exam
    exercises = course.exercises
    laboratories = course.laboratories
    project = course.project
    seminars = course.seminars

    details = {
        'name': name,
        'description': description,
        'ects': ects,
        'exam': exam,
        'exercises': exercises,
        'laboratories': laboratories,
        'project': project,
        'seminars': seminars
    }
    
    user = DBHelper.get_user(request)
    return render(request, 'course/course-details.html', {"role_obj": user.role, "course_details" : details})

def course_signup(request, id):
    course = Course.objects.get(course_id=id)
    user_role = DBHelper.get_user_role(request)
    user = DBHelper.get_user(request)
    if not user.courses.filter(pk=id).exists():
        if user_role == Values.USER_ROLE_STUDENT or user_role == Values.USER_ROLE_ACADEMIC:
            user_course = UserCourse(profile=user, course=course, accepted=0)
            user_course.save()
    return courses(request)

def course_signout(request, id):
    course = Course.objects.get(course_id=id)
    user = DBHelper.get_user(request)
    user_course = UserCourse.objects.get(profile=user, course=course)
    if user_course is not None and user_course.accepted == 0:
        user_course.delete()
    return courses(request)

def course_approvals(request, id):
    course = Course.objects.get(course_id=id)
    user_role = DBHelper.get_user_role(request)
    user = DBHelper.get_user(request)
    if user_role == Values.USER_ROLE_DEAN:
        user_courses = UserCourse.objects.filter(course=course)
        return render(request, 'course/course-approvals.html', {
            "role_obj": user.role,
            "course" : course,
            "user_courses": user_courses
        })
    else:
        return courses(request)

def course_approvals_approve(request, course_id, user_id):
    course = Course.objects.get(course_id=course_id)
    user_role = DBHelper.get_user_role(request)
    if user_role == Values.USER_ROLE_DEAN:
        profile = DBHelper.get_user_by_id(user_id)
        user_course = UserCourse.objects.get(profile=profile, course=course)
        user_course.accepted = 1
        user_course.save()
        return course_approvals(request, course_id)
    else:
        return courses(request)

def course_approvals_kick(request, course_id, user_id):
    course = Course.objects.get(course_id=course_id)
    user_role = DBHelper.get_user_role(request)
    if user_role == Values.USER_ROLE_DEAN:
        profile = DBHelper.get_user_by_id(user_id)
        user_course = UserCourse.objects.get(profile=profile, course=course)
        user_course.delete()
        return course_approvals(request, course_id)
    else:
        return courses(request)

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