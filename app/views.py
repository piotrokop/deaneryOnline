# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
    return render(request, 'course/create-course.html', {"form" : form})

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
            return render(request, 'course/courses.html')
    else:
        form = CourseForm(instance=course, initial=init)

    return render(request, 'course/create-course.html', {"form" : form, "edit": 1})

def courses(request):
    if request.user.is_authenticated():
        user_role = DBHelper.get_user_role(request)
        user = DBHelper.get_user(request)
        user_courses = UserCourse.objects.filter(profile=user)
        rest_courses = Course.objects.exclude(course_id__in=[c.course_id for c in user_courses])

        return render(request, 'course/courses.html', {
            "role" : user_role,
            "rest_courses" : rest_courses,
            "user_courses" : user_courses
        })
		
def grades(request):
	if request.user.is_authenticated():
		user = DBHelper.get_user(request)
		grades = UserGrade.objects.filter(student_user=user)
		course_set = Set()
		courses = []
		grade_set = (grade for grade in grades )
		for grade in grade_set:
			course_set.add(grade.course)
		for c in course_set:
			course = Course.objects.get(course_id=c)
			courses.append({'Name' : course.name ,'Id' : course.course_id , 'ECTS' : course.ects})
		for grade in grade_set:
			course = (c for c in courses if c['Id'] == grade.course)
			for c in course:
				c[grade.category]=grade.grade
		return render(request, 'course/grades.html', {
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

    return render(request, 'course/course-details.html', {"course_details" : details})

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
    if user_role == Values.USER_ROLE_DEAN:
        user_courses = UserCourse.objects.filter(course=course)
        return render(request, 'course/course-approvals.html', {
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
    return render(request, 'main.html')
	
	
def course_manage(request, id):
    course = Course.objects.get(course_id = id)
    user_courses = UserCourse.objects.filter(course=course, accepted=1)
    ManageCourseFormSet = formset_factory(ManageCourseForm)
    isvalid = ' '
    if request.method == 'POST':
        formset = ManageCourseFormSet(request.POST, request.FILES)
        if formset.is_valid():
            user_index = 0
            for form in formset:
                usergrade = form.save(commit=False)
                data = form.cleaned_data
                isvalid = str(isvalid) + str('  ,  ') + data.get('project')
                if request.POST.get('exercises') != None:
                    usergrade.grade = request.POST.get('exercises')
                    usergrade.is_final = False
                    usergrade.course_id = id
                    usergrade.category = 'exercises'
                    usergrade.professor_user_id = request.user.id
                    usergrade.student_user_id = user_courses[user_index].profile.user_id
                    usergrade.save()					
                if request.POST.get('laboratory') != None:
                    usergrade.grade = request.POST.get('laboratory')
                    usergrade.is_final = False
                    usergrade.course_id = id
                    usergrade.category = 'laboratory'
                    usergrade.professor_user_id = request.user.id
                    usergrade.student_user_id = user_courses[user_index].profile.user_id
                    usergrade.save()
                if request.POST.get('project') != None:
                    usergrade.grade = request.POST.get('project')
                    usergrade.is_final = False
                    usergrade.course_id = id
                    usergrade.category = 'project'
                    usergrade.professor_user_id = request.user.id
                    usergrade.student_user_id = user_courses[user_index].profile.user_id
                    usergrade.save()
                    isvalid = isvalid + 1
                if request.POST.get('seminar') != None:
                    usergrade.grade = request.POST.get('seminar')
                    usergrade.is_final = False
                    usergrade.course_id = id
                    usergrade.category = 'seminar'
                    usergrade.professor_user_id = request.user.id
                    usergrade.student_user_id = user_courses[user_index].profile.user_id
                    usergrade.save()
                if request.POST.get('exam') != None:
                    usergrade.grade = request.POST.get('exam')
                    usergrade.is_final = False
                    usergrade.course_id = id
                    usergrade.category = 'exam'
                    usergrade.professor_user_id = request.user.id
                    usergrade.student_user_id = user_courses[user_index].profile.user_id
                    usergrade.save()
                if request.POST.get('final_grade') != None:
                    usergrade.grade = request.POST.get('final_grade')
                    usergrade.is_final = False
                    usergrade.course_id = id
                    usergrade.category = 'finalgrade'
                    usergrade.professor_user_id = request.user.id
                    usergrade.student_user_id = user_courses[user_index].profile.user_id
                    usergrade.save()
                user_index += 1
            #return redirect('courses')
    
    ManageCourseFormSet = formset_factory(ManageCourseForm, extra = 2)
    formset = ManageCourseFormSet()
    return render(request, 'course/course-manage.html', {"course": course, "user_courses": user_courses, "formset": formset, "isvalid": isvalid,})


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