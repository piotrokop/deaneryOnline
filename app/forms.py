from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course

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
    role_id = forms.ChoiceField(choices=ROLE_CHOICES)
    role_id.label="Role"

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role_id', 'password1', 'password2', )