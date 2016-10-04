from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<lang>[a-zA-Z]{2})/$', views.index, name='index-lang'),
]
