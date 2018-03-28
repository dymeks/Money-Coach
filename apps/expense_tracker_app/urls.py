from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^import$', views.import_sheet),
    url(r'^display$', views.display_docs),
    url(r'^edit/(?P<t_id>\d+)$', views.edit),
    url(r'^modify/(?P<t_id>\d+)$', views.modify),
]
