from django import forms

from .models import Course

class CourseForm(forms.ModelForm):
	if_exer = forms.BooleanField(required = False,label = 'if_exer')
	if_lab = forms.BooleanField(required = False,label = 'if_lab')
	if_proj = forms.BooleanField(required = False,label = '')
	if_sem = forms.BooleanField(required = False,label = '')
	exercises = forms.IntegerField(required = False,label = 'Exercises')
	laboratories = forms.IntegerField(required = False,label = 'Laboratories')
	project = forms.IntegerField(required = False,label = 'Project')
	seminars = forms.IntegerField(required = False,label = 'Seminars')
	exam = forms.BooleanField(required = False,label = 'Exam')
	class Meta:
		model = Course
		fields = ('name','description','ects',)