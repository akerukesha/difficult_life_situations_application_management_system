from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_cases/$', views.create_cases, name='create_cases'),
    url(r'^update_cases/$', views.update_cases, name='update_cases'),
    url(r'^get_all_cases/$', views.get_all_cases, name='get_all_cases'),
 	url(r'^get_priorities/$', views.get_priorities, name='get_priorities'),   
]