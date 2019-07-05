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
        ("P_A", "Parrot Auto"),
    )
    name = models.CharField(max_length=40,null=False,blank=False)
    tag = models.CharField(choices=TAG_CHOICES,max_length=4,null=False,blank=False)
    arg = models.IntegerField(unique=True,blank=False,null=False)
    priority = models.IntegerField(blank=False,null=False,default=10)
    isVoice = models.BooleanField(default = False)
    voiceFile = models.FileField(blank = True)
    performTime = models.IntegerField(default=5) #in second

    def __str__(self):
        return self.tag + ": " + self.name


class Patient(models.Model):
    first_name = models.CharField(max_length=40,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=False,blank=False)
    phone_regex = RegexValidator(regex=r'^\+?0?\d{9,15}$',
                                 message="شماره تلفن خود را در فرمت مناسب بنویسید")
    phone_number = models.CharField(max_length=17,null=False,blank=False, validators=[RegexValidator])  # validators should be a list
    birthYear = models.IntegerField(null=True, blank=True)
    gender = models.BooleanField(null=False, blank=False)

    medicalHistory = (
        ("ADHD", "ADHD"),
        ("Normal", "نرمال"),
        ("Autism", "اتیسم"),
        ("Undefined", "تعیین نشده"),
    )
    medicalInfo = models.CharField(choices=medicalHistory, max_length=10, null=False, blank=False)
    personIDRegex = RegexValidator(regex=r'^\d{10}$',
                                 message="کد ملی عددی ۱۰ رقمی باید باشد")
    personID = models.CharField(validators=[personIDRegex], null=False, blank=False, unique=True, max_length=10)

    login_status = models.BooleanField(default=False)
    last_activity = models.BigIntegerField(default=getTime)

    stages = (
        ("NS", "not started"),
        ("PG", "pregame"),
        ("W", "weel"),
        ("P", "parrot"),
        ("D", "done"),
    )
    stage = models.CharField(choices=stages,max_length=2)

    def __str__(self):
        return self.personID



# use authentication backend    and    uniqetogether for not use of AbstractUser and username pass for login
