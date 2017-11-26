from django.contrib.auth.models import User
from app.models import UserRole, Course, Profile


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
        user_id = User.objects.get(pk=request.user.id).pk
        user_role = User.objects.get(pk=request.user.profile.role_id).pk
        return user_role