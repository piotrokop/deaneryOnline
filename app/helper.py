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