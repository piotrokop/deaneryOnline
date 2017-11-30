from django.core.management.base import BaseCommand, CommandError
from app.models import User
from app.models import UserRole
from app.models import Profile
import os
import cmd

class MessageStyles:
    warning = '\033[91m'
    bold = '\033[1m'
    original = '\033[0m'

class Command(BaseCommand):

    def ask_for_data(self, data, label):
        while data == "":
            data = raw_input(label)
            if data == "":
                print MessageStyles.warning + MessageStyles.bold
                print "This field cannot be blank." + MessageStyles.original

        return data

    def handle(self, *args, **options):

        first_name, last_name = "", ""
        first_name = self.ask_for_data(first_name, "First name: ")
        last_name = self.ask_for_data(last_name, "Last name: ")

        os.system("python manage.py createsuperuser")

        dean_role = UserRole.objects.get(pk=3)
        user_id = User.objects.latest('id').id
        user = User.objects.get(pk=user_id)

        user.profile.role_id = dean_role
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        print "Dean created successfully."


