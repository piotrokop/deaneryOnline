from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from grade.models import UserGrade
		
		
		
class ManageCourseForm(forms.ModelForm):
	GRADE_CHOICES = (
        ('None', 'None'),
		(2.0, '2.0'),
		(3.0, '3.0'),
		(3.5, '3.5'),
		(4.0, '4.0'),
		(4.5, '4.5'),
		(5.0, '5.0'),
	)
	exercises = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	laboratories = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	project = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	seminars = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	exam = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	final_grade = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	
	class Meta:
		model = UserGrade
		fields = ('exercises', 'laboratories', 'project', 'seminars', 'exam', 'final_grade', )