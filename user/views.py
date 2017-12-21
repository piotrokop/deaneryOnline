# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import formset_factory
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import UserRole, Profile
from django.contrib.auth.models import User
from app.helper import Values, DBHelper
from sets import Set
from grade.models import UserGrade
from course.forms import CourseForm
from user.models import UserCourse

@login_required()
def createview(request):
    user = DBHelper.get_user(request)
    return render(request, 'main.html', {"role_obj": user.role})


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