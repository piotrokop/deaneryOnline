BASIC STEPS TO RUN THE PROJECT:
1. Install PostgreSQL
2. PotgreSQL config :
    database name: deanery
    database user: deanery
    database user password: deanery098
    database ip: localhost
    database port: 5432
3. python manage.py migrate
4. python manage.py loaddata app/static/data/initial_user_roles.json
5. python manage.py runserver

0. AFTER PULL:
usuwamy bazę deanery i tworzymy nową deanery w pgadmin(trwa to sekundkę w pgadmin, prawym na bazę i drop, a następnie prawym na databases i create)
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata app/static/data/initial_user_roles.json
python manage.py loaddata app/static/data/initial_users.json
python manage.py loaddata app/static/data/initial_profiles.json
python manage.py loaddata app/static/data/initial_courses.json
i już działa

1. LOGGING

CREATING SUPERUSER:
python manage.py createsuperuser

CREATING ANY OTHER USER:
-go to http://127.0.0.1:8000/admin/

USE:
http://127.0.0.1:8000/accounts/login/

CREATING DEAN:
python manage.py createdeanuser

2. CLEAN DATABASE:
python manage.py flush


3. ENTIRE FLOW TO PREPARE SAMPLE DATABASE:
python manage.py makemigrations
python manage.py migrate

python manage.py loaddata app/static/data/initial_user_roles.json
python manage.py loaddata app/static/data/initial_users.json
python manage.py loaddata app/static/data/initial_profiles.json
python manage.py loaddata app/static/data/initial_courses.json

hasło do userów:
test1234

4. DUMPING DATA FOR USERS TABLE:
after creating users manually
./manage.py dumpdata auth.user --indent 2 > user.json
