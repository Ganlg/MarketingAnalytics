from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^sentiment/$', views.sentiment, name='sentiment'),
    url(r'^ajax-sentiment/$', views.ajax_sentiment, name='ajax-sentiment')
]
