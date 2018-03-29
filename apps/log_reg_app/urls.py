from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.land),
    url(r'^log/reg$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
]