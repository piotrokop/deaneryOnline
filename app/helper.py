from django.contrib.auth.models import User
from user.models import UserRole, Profile


class Values:
    USER_ROLE_STUDENT = 1
    USER_ROLE_ACADEMIC = 2
    USER_ROLE_DEAN = 3

class DBHelper:
    @staticmethod
    def get_user(request):
        return Profile.objects.get(pk=request.user.id)

    @staticmethod
    def get_user_by_id(id):
        return Profile.objects.get(pk=id)

    @staticmethod
    def get_user_role(request):
        user_role = DBHelper.get_user(request).role.pk
        return user_role
		
    @staticmethod
    def add_extra_params_to_course(request,course):
        if request.POST.get('if_exer') and request.POST.get('exercises'):
            course.exercises = request.POST.get('exercises')
        else:
            course.exercises = None
        if request.POST.get('if_lab') and request.POST.get('laboratories'):
            course.laboratories = request.POST.get('laboratories')
        else:
            course.laboratories = None
        if request.POST.get('if_proj') and request.POST.get('project'):
            course.project = request.POST.get('project')
        else:
            course.project = None
        if request.POST.get('if_sem') and request.POST.get('seminars'):
            course.seminars = request.POST.get('seminars')
        else:
            course.seminars = None