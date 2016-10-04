from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^register/$', views.account_register, name='register'),
    url(r'^login/$', views.account_login, name='login')

]
