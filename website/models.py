from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class command(models.Model):
    TAG_CHOICES = (
        ("P_S1", "Parrot Senario 1"),
        ("P_S2", "Parrot Senario 2"),
        ("P_M", "Parrot Movment"),
        ("W", "Weel"),
    )
    name = models.CharField(max_length=40,null=False,blank=False)
    tag = models.CharField(choices=TAG_CHOICES,null=False,blank=False)
    arg = models.IntegerField()

class person(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False)  # validators should be a list
    login_status = models.BooleanField(default=False)
    last_activity = models.BigIntegerField(default=0)

    age = models.IntegerField()
    # and so on

    class Meta:
        unique_together = (("first_name", "last_name","phone_number"),)




# use authentication backend    and    uniqetogether for not use of AbstractUser and username pass for login
