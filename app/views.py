# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def courses(request):
	return render(request, 'app/courses.html', {})

@login_required()
def createview(request):
    html = "<html><body>You are logged in!</body></br> <a href=\"/logout\">Logout</a></html>"
    return HttpResponse(html)
