# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..log_reg_app.models import User

# Create your models here.
class Document(models.Model):
    document = models.FileField(upload_to='documents/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="files_uploaded")

    
class Transaction(models.Model):
    date_of_purchase = models.DateField('date purchased')
    company = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    document = models.ForeignKey(Document, related_name="transactions_of", null=True, blank=True)
    user = models.ForeignKey(User, related_name="personal_transactions", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.company

class Goal(models.Model):
    title = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=19, decimal_places=2)
    current_amount = models.DecimalField(max_digits=19, decimal_places=2)
    user = models.ForeignKey(User, related_name="user_goals")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)