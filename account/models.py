from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import Service


class User(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=30, blank=True)
    postal = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=50, blank=True)
    service = models.ForeignKey(Service, null=True, blank=True)
    service_expire= models.DateTimeField('Service expire on', null=True, blank=True)

    activation_key = models.CharField(max_length=40, null=True)
    key_expires = models.DateTimeField(null=True)
    email_verified = models.BooleanField(default=False)
