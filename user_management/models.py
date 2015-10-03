from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='usermanagement_user')
    confirmation_code = models.CharField(max_length=128, null=True)
    reset_code = models.CharField(max_length=128, null=True)

class AppKey(models.Model):
    key = models.CharField(max_length=38)
    active = models.BooleanField()
    expiry_date = models.DateField()
    owner = models.ForeignKey(UserProfile, null=True)
