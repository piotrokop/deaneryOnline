"""deaneryOnline URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
#from app import views
from app.views import createview, courses, create_course, edit_course, course_details, course_signup, course_signout, course_approvals, course_approvals_approve, course_approvals_kick, signup, course_manage
from app.views import grades
urlpatterns = [
    url(r'^login/', auth_views.login, name='login'),
    url(r'^accounts/login/', auth_views.login, name='accounts-login'),
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^signup/', signup, name='signup'),
    url(r'^accounts/profile/', createview),
    url(r'^$', createview, name='main'),
    url(r'^admin/', admin.site.urls),
    url(r'^courses/', courses, name='courses'),
    url(r'^create-course/', create_course, name='create-course'),
    url(r'^edit-course/(?P<id>[0-9]+)/', edit_course, name='edit-course'),
    url(r'^course-details/(?P<id>[0-9]+)/', course_details, name='course-details'),
    url(r'^course/signup/(?P<id>[0-9]+)/', course_signup, name='course-signup'),
    url(r'^course/signout/(?P<id>[0-9]+)/', course_signout, name='course-signout'),
    url(r'^course/approvals/(?P<id>[0-9]+)/', course_approvals, name='course-approvals'),
    url(r'^course/approvals/approve/(?P<course_id>[0-9]+)/(?P<user_id>[0-9]+)', course_approvals_approve, name='course-approvals-approve'),
    url(r'^course/approvals/kick/(?P<course_id>[0-9]+)/(?P<user_id>[0-9]+)', course_approvals_kick, name='course-approvals-kick'),
	url(r'^course/manage/(?P<id>[0-9]+)/', course_manage, name='course-manage'),
	url(r'^grades/', grades, name='grades'),
]