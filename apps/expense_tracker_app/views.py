# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def home(request):
    response = "THis will display the success page/home page after login/registration is successful"
    return HttpResponse(response)