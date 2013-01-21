from django.db import models

class Account(models.Model):
    username        = models.CharField(max_length=30, unique=True)
    password        = models.CharField(max_length=30)
    phone_number    = models.CharField(max_length=30, blank=True, null=True)