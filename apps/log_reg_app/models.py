# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        result = {
            'status': False
        }
        errors = {}
        if len(postData['first_name']) < 3 or len(postData['last_name']) < 3:
            errors["name_length"] = "User first and last name must be at least 2 characters"

        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors["name_alpha"] = "User first and last name must contain alphabetical characters only"
        
        if len(postData['password']) < 8:
            errors["pass_length"] = "Password must be at least 8 characters"
        
        if postData['password'] != postData['password_conf']:
            errors["pass_match"] = "Password and password confirmation must match"
        
        e_check = User.objects.filter(email = postData['email'])
        if len(e_check):
            errors["curr_email"] = "This email had already been registered"

        if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']):
            errors["email_format"] = "Must input valid email"
        
        if len(postData['bday']) == 0:
            errors['enter_bday'] = "Please enter date of birth to register"

        result['errors'] = errors
        if len(errors) == 0:
            result['status'] = True
            result['user'] = self.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
        return result
    
    def login_validator(self, postData):
        result = {
            'status': False
        }
        errors = {}
        e_log = User.objects.filter(email = postData['email'])
        if len(e_log):            
            if not bcrypt.checkpw(postData['password'].encode(), e_log[0].password.encode()):
                errors["pass_log"] = "Incorrect password"
        else:
            errors["email_exist"] = "This email has not been registered"

        result['errors'] = errors
        if len(errors) == 0:
            result['status'] = True
            result['user'] = self.get(email = postData['email'])
        return result

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    birthday = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)  

    objects = UserManager()

    def __repr__(self):
        return "<User object: {} {}, email: {}>".format(self.first_name, self.last_name, self.email)