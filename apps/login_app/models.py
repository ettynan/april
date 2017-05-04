from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re, bcrypt
# from bcrypt import hashpw

FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]*$)")
# Create your models here.

class UserManager(models.Manager):
    def validate_user(self, data):
        print "models user email validate", data
        errors = []

        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        confirm_pw = data['confirm_pw']
        
        if not (FIRST_NAME_REGEX.match(data['first_name']) and len(data['first_name']) > 1):
            errors.append('First name must be at least 2 characters and no numbers or special characters')
        if not (LAST_NAME_REGEX.match(data['last_name']) and len(data['last_name']) > 1):
            errors.append('Last name must be at least 2 characters and no numbers or special characters')
        if len(data['email']) < 5:
            errors.append('Email field must be filled out and greater than 5 characters')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Invalid email')
        if len(data['password']) < 1:
            errors.append('Password is required and greater than 8 characters')
        elif len(data['password']) < 8:
            errors.append('Password must be greater than 8 characters')
        if data['password'] != data['confirm_pw']:
            errors.append('Passwords must match')
        if User.objects.filter(email=data['email']).exists():
            errors.append('Email already in use, please login')
        print errors
        if errors:
            return(False, errors)
        else:
            user_person = self.create(
                first_name=first_name, 
                last_name=last_name, 
                email = email,
                password = bcrypt.hashpw((data['password']).encode(),bcrypt.gensalt())
                )
            print user_person
            return(True, user_person)

    def validate_login(self, data):
        print'data', data
        errors = []
        if len(data['email']) < 1:
            errors.append('Email is required')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Invalid email')
        if len(data['password']) < 1:
            errors.append('Password required')
        if not errors:
            try:
                user = self.get(email=data['email'])
                if bcrypt.hashpw(data['password'].encode(),user.password.encode()) == user.password.encode():
                    return (True, user)
            except:
                errors.append('invalid credentials')
        return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __unicode__(self):
        return unicode(self.first_name)

