from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from time import time

# Create your models here.
def getTime():
    return time()

class command(models.Model):
    TAG_CHOICES = (
        ("P_S1", "Parrot Senario 1"),
        ("P_S2", "Parrot Senario 2"),
        ("P_M", "Parrot Movment"),
        ("W", "Weel"),
    )
    name = models.CharField(max_length=40,null=False,blank=False)
    tag = models.CharField(choices=TAG_CHOICES,max_length=4,null=False,blank=False)
    arg = models.IntegerField(unique=True,blank=False,null=False)
    priority = models.IntegerField(blank=False,null=False)
    isVoice = models.BooleanField(default = False)
    voiceFile = models.FileField(blank = True)

class person(models.Model):
    first_name = models.CharField(max_length=40,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=False,blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17,null=False,blank=False)  # validators should be a list
    login_status = models.BooleanField(default=False)
    last_activity = models.BigIntegerField(default=getTime)

    age = models.IntegerField(null=True,blank=True)
    # and so on

    class Meta:
        unique_together = (("first_name", "last_name","phone_number"),)




# use authentication backend    and    uniqetogether for not use of AbstractUser and username pass for login
