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
    price = models.DecimalField(max_digits=19, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.question_text