from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^register/$', views.account_register, name='register'),
    # url(r'^register-done/$', views.account_register_done, name='register-done'),
    url(r'^activate/(?P<key>.{40})/$', views.account_activate, name='activate'),
    url(r'^send-activation/$', views.account_send_activation, name='send-activation'),

    url(r'^login/$', views.account_login, name='login'),

    url(r'^forget-password/$', views.account_forget_password, name='forget-password'),
    url(r'^reset-password/$', views.account_reset_password, name='reset-password'),
    url(r'^reset-password-done', views.account_reset_password_done, name='reset-password-done'),
    url(r'^reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        views.account_reset_password_confirm, name='reset-password-confirm'),
    # url(r'^reset-password-confirm/(?P<token>[0-9A-Za-z]+-.+)/$',
    #     views.account_reset_password_confirm, name='reset-password-confirm'),
    url(r'^forget-username/$', views.account_forget_username, name='forget-username'),
    url(r'^get-username/$', views.account_get_username, name='get-username'),



]
