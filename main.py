from os import environ

1. pip install django
2. pip install djangorestframework
3. django_admin startproject mysite
4. cd (mysite)
5. python manage.py startapp (hotel_app)
6. settings.py
     6.1  .env
     6.2  gitignore <- .env
     6.3  pip install python-dotenv
7. models.py -> бекенд кандай маалыматтар менен иштеп база данныхка кандай
   маалыматтарды сактай турган болсок логика ушул жака жазылат
8.python manage.py makemigrations -> migrate
9.python manage.py createsuperuser