# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import formset_factory
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from grade.models import UserGrade
from user.forms import SignUpForm
from user.models import UserRole, Profile
from django.contrib.auth.models import User
from app.helper import Values, DBHelper
from course.forms import CourseForm
from course.models import Course
from user.models import UserCourse

# Create your views here.
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        course = form.save(commit=False)
        if request.POST.get('exam'):
            course.exam = 1
        course.save()
        return redirect(courses);
    else:
        form = CourseForm()
    return render(request, 'create-course.html', {"form" : form})

def edit_course(request, id):
    course = Course.objects.get(course_id=id)
    init = {
        'exam': (True if course.exam == 1 else False),
        'exercises': course.exercises,
        'laboratories': course.laboratories,
        'project': course.project,
        'seminars': course.seminars,
        'if_exer': (True if course.exercises else False),
        'if_lab': (True if course.laboratories else False),
        'if_proj': (True if course.project else False),
        'if_sem': (True if course.seminars else False)
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
                if request.POST.get('exam'):
                    course.exam = 1
                course.save()
                return redirect(courses)
    else:
        form = CourseForm(instance=course, initial=init)
    return render(request, 'create-course.html', {"form" : form, "edit": 1})

@login_required()
def courses(request):
    if request.user.is_authenticated():
        user_role = DBHelper.get_user_role(request)
        user = DBHelper.get_user(request)
        user_courses = UserCourse.objects.filter(profile=user)
        rest_courses = Course.objects.exclude(course_id__in=[c.course_id for c in user_courses])

        user = DBHelper.get_user(request)
        return render(request, 'courses.html', {
            "role_obj": user.role,
            "role" : user_role,
            "rest_courses" : rest_courses,
            "user_courses" : user_courses
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
    return render(request, 'course-details.html', {"role_obj": user.role, "course_details" : details})

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
        return render(request, 'course-approvals.html', {
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
