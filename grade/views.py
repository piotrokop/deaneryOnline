# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import formset_factory
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from user.models import Profile
from django.contrib.auth.models import User
from app.helper import Values, DBHelper
from .models import UserGrade
from grade.forms import ManageCourseForm
from course.models import Course
from user.models import UserCourse

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
        sum,pkt =0.0,0
        for c in courses:
            if 'final_grade' in c:
                sum += float(c['final_grade']) * c['ECTS']
                pkt += c['ECTS'] if c['final_grade'] else 0
        return render(request, 'grades.html', {
            "role_obj": user.role,
            "gradeList" : courses,
            "average" : "{0:.2f}".format((sum/pkt) if pkt else 0)
        })



def course_manage(request, id):
    course = Course.objects.get(course_id = id)
    user_courses = UserCourse.objects.filter(course=course, accepted=1, profile__role=1)
    ManageCourseFormSet = formset_factory(ManageCourseForm, extra = 0)
    zipped = []
    users_list = [(user_course.profile.user.first_name, user_course.profile.user.last_name) for user_course in user_courses]
    if request.method == 'POST':
        formset = ManageCourseFormSet(request.POST)
        if formset.is_valid():
            user_index = 0
            for form in formset:
                form.save(course, user_courses, user_index, request.user.id, id)
                zipped.append((form, users_list[user_index]))
                user_index += 1
    else:
        user_index = 0
        initial_grades = []
        for user_course in user_courses:
            profile = user_course.profile
            grades = UserGrade.objects.filter(student_user = profile, course=course)
            grades_dict = {}
            for grade in grades:
                grades_dict[grade.category] = grade.grade
            initial_grades.append(grades_dict)
        formset = ManageCourseFormSet(initial=initial_grades)
        for form in formset:
            zipped.append((form, users_list[user_index]))
            user_index += 1

    user = DBHelper.get_user(request)
    return render(request, 'course-manage.html', {"role_obj": user.role, "course": course, "zipped": zipped, "formset": formset, "user_courses": user_courses})
