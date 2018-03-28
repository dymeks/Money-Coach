from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^import$', views.import_sheet),
    url(r'^display$', views.display_docs),
]
