# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import Course

# Create your views here.
def courses(request):
	user_role = 2
	courses = Course.objects.all()
	return render(request, 'app/courses.html', {"role" : user_role, "all_courses" : courses})

@login_required()
def createview(request):
    html = "<html><body>You are logged in!</body></br> <a href=\"/logout\">Logout</a></html>"
    return HttpResponse(html)
