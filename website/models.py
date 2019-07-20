from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from time import time
from website import myexceptions
from django.core.exceptions import ValidationError
from website import settings
from threading import Timer
def getTime():
    return time()

def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)

class Duration(models.Model):
    def clean(self):
        validate_only_one_instance(self)

    game_duration_minutes = models.SmallIntegerField()
    wheel_duration_minutes = models.SmallIntegerField()
    parrot_duration_minutes = models.SmallIntegerField()

#    done_duration_minutes = models.SmallIntegerField(default= 0)

    def __str__(self):
        return 'Duration For Different Stages'

    @staticmethod
    def get():
        try:
            return Duration.objects.all()[0]
        except IndexError:
            return Duration.objects.create(game_duration_minutes = settings.DEFAULT_GAME_DURATION, wheel_duration_minutes = settings.DEFAULT_WHEEL_DURATION, 
                parrot_duration_minutes= settings.DEFAULT_PARROT_DURATION)
        
    def game_duration(self): return self.game_duration_minutes * 60
    def wheel_duration(self): return self.wheel_duration_minutes * 60
    def parrot_duration(self): return self.parrot_duration_minutes * 60
    def stage_duration(self, stage_name):
        if stage_name == settings.GAME_STAGE:
            return self.game_duration()
        elif stage_name == settings.WHEEL_STAGE:
            return self.wheel_duration()
        elif stage_name == settings.PARROT_STAGE:
            return self.parrot_duration()
        elif stage_name == settings.DONE_STAGE:
            return 0
        else: raise ValueError('No stage is named ' + stage_name)

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
    genderValues = (
        ("مرد", "مرد"),
        ("زن", "زن"),
    )
    
    gender = models.CharField(null=False, blank=False, max_length=10, choices=genderValues)

    medicalHistory = (
        ("ADHD", "ADHD"),
        ("نرمال", "نرمال"),
        ("اتیسم", "اتیسم"),
        ("تعیین نشده", "تعیین نشده"),
    )
    medicalInfo = models.CharField(choices=medicalHistory, max_length=10, null=False, blank=False)
    personIDRegex = RegexValidator(regex=r'^\d{10}$',
                                 message="کد ملی عددی ۱۰ رقمی باید باشد")
    personID = models.CharField(validators=[personIDRegex], null=False, blank=False, unique=True, max_length=10)

    login_status = models.BooleanField(default=False)
    last_activity = models.BigIntegerField(default=getTime)


    def __str__(self):
        return self.personID

    def current_session(self):
        return self.diagnosesession_set.get(expired= False)

    def check_session(self):
        if not self.diagnosesession_set.filter(expired= False):
            return False
        return True

    def start_session(self):
        now = time()
        default_stage = Stage.objects.create(start_time= now, duration= Duration.get().game_duration(), name= settings.GAME_STAGE)
        started_session = DiagnoseSession.objects.create(patient= self, start_time= now, stage= default_stage)

        t = Timer(default_stage.duration, started_session.auto_next_stage)
        t.daemon = True
        t.start()

  
    def end_session(self):
        current_session = self.current_session()
        current_session.expired = True
        current_session.save()

    def pause_session(self):
        current_session = self.current_session()
        current_session.paused = True
        current_session.save()
    
    def resume_session(self):
        current_session = self.current_session()
        current_session.paused = False
        current_session.save()
        t = Timer(current_session.stage.duration, current_session.auto_next_stage)
        t.daemon = True
        t.start()
        
    # TODO Save session duration when user logs out
    # TODO Expire session when its done
    def end_finished_session(self):
        current_session = self.current_session()
        if current_session.stage.name == settings.DONE_STAGE:
            current_session.expired = True
            current_session.save()

    def change_stage(self, new_stage):
        self.current_session().change_stage(new_stage)


    @staticmethod
    def current_patient():
        return Patient.objects.get(login_status= True)

class Stage(models.Model):
    start_time = models.BigIntegerField(null= False)
    duration = models.IntegerField(null= False)
    stages = (
        (settings.NOT_STARTED_STAGE, "not started"),
        (settings.GAME_STAGE, "game"),
        (settings.WHEEL_STAGE, "Wheel"),
        (settings.PARROT_STAGE, "parrot"),
        (settings.DONE_STAGE, "done"),
    )
    name = models.CharField(choices=stages,max_length=2, default= settings.NOT_STARTED_STAGE)
    expired = models.BooleanField(null= False, default= False)
    auto_update = models.BooleanField(default= True)

    def renew(self):
        if self.expired:
            raise myexceptions.StageExpired("Can\'t Renew Expired Stage")
        
        self.duration += Duration.get().stage_duration(self.name)
        self.save()

    def check_expired(self):
        if self.start_time + self.duration > time():
            self.expired = True
            self.save()
            return True
        
        return False


class DiagnoseSession(models.Model):
    patient = models.ForeignKey(Patient, on_delete= models.CASCADE)
    start_time = models.BigIntegerField(null= False, default= False)
    finish_time = models.BigIntegerField(default= 0)
    
    stage = models.ForeignKey(Stage, on_delete= models.DO_NOTHING)

    diagnose_result = (
        ('اتیسم به احتمال قوی', 'اتیسم به احتمال قوی'),
        ('اتیسم به احتمال ضعیف', 'اتیسم به احتمال قوی'),
        ('عدم تشخیص اتیسم', 'اتیسم به احتمال قوی'),
        ('اعلام نشده', 'اعلام نشده')
    )
    expertsystem_judgement = models.CharField(choices= diagnose_result, max_length= 64, default= diagnose_result[3][0])

    paused = models.BooleanField(default= False)
    expired = models.BooleanField(default= False)

    def change_stage(self, new_stage):
        self.stage.start_time = time()
        self.stage.duration= Duration.get().stage_duration(new_stage)
        self.stage.name= new_stage
        self.stage.expired = False
        self.stage.auto_update = True
        self.stage.save()   
        self.save()

    def auto_next_stage(self):
        if not self.stage.auto_update or self.paused:
            return
        self.change_stage(settings.NEXT_STAGE[self.stage.name])
        if self.stage.name != settings.DONE_STAGE:
            t = Timer(self.stage.duration, self.auto_next_stage)
            t.daemon = True
            t.start()
        else: 
            self.expired = True
            self.save()

    @staticmethod
    def check_active_session():
        try:
            DiagnoseSession.objects.get(expired= False, paused= False)
            return True
        except DiagnoseSession.DoesNotExist:
            return False



class ToyCar(models.Model):
    session = models.ForeignKey(DiagnoseSession, on_delete=models.CASCADE)
    time = models.BigIntegerField(null= False)
    ac_x = models.BigIntegerField(null= False)
    ac_y = models.BigIntegerField(null= False)
    ac_z = models.BigIntegerField(null= False)
    encode1 = models.BigIntegerField(null= False)
    encode2 = models.BigIntegerField(null= False)

#    class Meta:
#       unique_together = ('session', 'time', )


class Game(models.Model):
    dummy = models.IntegerField(default=0, null=True, blank= True)
# use authentication backend    and    uniqetogether for not use of AbstractUser and username pass for login


"""
    stages = (
        (settings.NOT_STARTED_STAGE, "not started"),
        (settings.GAME_STAGE, "game"),
        (settings.WHEEL_STAGE, "Wheel"),
        (settings.PARROT_STAGE, "parrot"),
        ("D", "done"),
    )
    stage = models.CharField(choices=stages,max_length=2)
"""