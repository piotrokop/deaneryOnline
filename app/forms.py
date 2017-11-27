from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course
from .models import UserGrade

class CourseForm(forms.ModelForm):
    if_exer = forms.BooleanField(required=False, label='if_exer')
    if_lab = forms.BooleanField(required=False, label='if_lab')
    if_proj = forms.BooleanField(required=False, label='')
    if_sem = forms.BooleanField(required=False, label='')
    exercises = forms.IntegerField(required=False, label='Exercises')
    laboratories = forms.IntegerField(required=False, label='Laboratories')
    project = forms.IntegerField(required=False, label='Project')
    seminars = forms.IntegerField(required=False, label='Seminars')
    exam = forms.BooleanField(required=False, label='Exam')
    class Meta:
        model = Course
        fields = ('name', 'description', 'ects')


class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        (1, 'Student'),
        (2, 'Academic'),
    )
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2', )
		
class ManageCourseForm(forms.ModelForm):
	GRADE_CHOICES = (
		(2.0, '2.0'),
		(3.0, '3.0'),
		(3.5, '3.5'),
		(4.0, '4.0'),
		(4.5, '4.5'),
		(5.0, '5.0'),
		(None, 'None'),
	)
	exercises = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	laboratory = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	project = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	seminar = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	exam = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	final_grade = forms.ChoiceField(choices=GRADE_CHOICES, required = False)
	
	class Meta:
		model = UserGrade
		fields = ('exercises', 'laboratory', 'project', 'seminar', 'exam', 'final_grade', )