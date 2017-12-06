from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from grade.models import UserGrade
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