from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from course.models import Course
from decimal import Decimal
from django.core.validators import EMPTY_VALUES

class CourseForm(forms.ModelForm):
    if_exer = forms.BooleanField(required=False, label='if_exer')
    if_lab = forms.BooleanField(required=False, label='if_lab')
    if_proj = forms.BooleanField(required=False, label='')
    if_sem = forms.BooleanField(required=False, label='')
    #exercises = forms.IntegerField(required=False, label='Exercises')
    #laboratories = forms.IntegerField(required=False, label='Laboratories')
    #project = forms.IntegerField(required=False, label='Project')
    #seminars = forms.IntegerField(required=False, label='Seminars')
    exam = forms.BooleanField(required=False, label='Exam')
    class Meta:
        model = Course
        fields = ('name', 'description', 'ects', 'exercises', 'laboratories', 'project', 'seminars')
        
    def clean(self):
        cleaned_data=super(CourseForm, self).clean()
        is_active = cleaned_data.get('if_exer', False)
        if not is_active:
            self.cleaned_data['exercises'] = None
        is_active = cleaned_data.get('if_lab', False)
        if not is_active:
            self.cleaned_data['laboratories'] = None
        is_active = cleaned_data.get('if_proj', False)
        if not is_active:
            self.cleaned_data['project'] = None
        is_active = cleaned_data.get('if_sem', False)
        if not is_active:
            self.cleaned_data['seminars'] = None
                
                
        return self.cleaned_data