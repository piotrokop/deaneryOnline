# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import formset_factory
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from user.models import UserRole, Profile
from django.contrib.auth.models import User
from app.helper import Values, DBHelper
from grade.models import UserGrade
from course.forms import CourseForm
from .models import UserCourse

@login_required()
def createview(request):
    user = DBHelper.get_user(request)
    return render(request, 'main.html', {"role_obj": user.role})