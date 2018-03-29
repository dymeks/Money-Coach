from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^options$', views.options),
    url(r'^import$', views.import_sheet),
    url(r'^display$', views.display_docs),
    url(r'^history$', views.history),
    url(r'^pie_chart$', views.pie_chart),
    url(r'^graph$', views.graph),
    url(r'^edit/(?P<t_id>\d+)$', views.edit),
    url(r'^modify/(?P<t_id>\d+)$', views.modify),
    url(r'^add/manual$', views.add_manual),

]
