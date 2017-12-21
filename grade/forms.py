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
        fields = ('exercises', 'laboratories', 'project', 'seminars', 'exam', 'final_grade')
        
    def save(self, course, user_courses, user_index, user_id, course_id):
        data = self.cleaned_data
        for field in self:
            if data[field.name] != 'None' and data[field.name] != '' and (field.name == 'final_grade' or getattr(course, field.name) > 0):
                usergrade, created = UserGrade.objects.get_or_create(
                    category=field.name,
                    student_user_id=user_courses[user_index].profile.user_id,
                    course_id=course_id,
                    defaults={'grade': 3.0, 'is_final': False, 'professor_user_id': user_id}
                )
                if created:
                    usergrade.is_final = True
                    usergrade.course_id = course_id
                    usergrade.category = field.name
                    usergrade.professor_user_id = user_id
                    usergrade.student_user_id = user_courses[user_index].profile.user_id
                usergrade.grade = data[field.name]
                usergrade.save()