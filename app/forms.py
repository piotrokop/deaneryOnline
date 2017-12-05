from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserGrade
from decimal import Decimal


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