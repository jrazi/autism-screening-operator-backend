#!/usr/bin/env python
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route,detail_route
from website import serializer,models, settings
from website.permissions import *
from website.authentication import PersonAuthentication
from website.settings import ros
from rest_framework import mixins
import json
from django.http import HttpResponse
from django.db import IntegrityError
import os
from os.path import expanduser
import datetime






# import rospy
# from std_msgs.msg import String

# parrot_command_name = rospy.Publisher('web/parrot_command_name', String, queue_size=10)
# parrot_command = rospy.Publisher('web/parrot_commands', String, queue_size=10)
# parrot_voice_commands = rospy.Publisher('web/parrot_voice_commands', String, queue_size=10)
# patient_uid = rospy.Publisher('web/patient_uid', String, queue_size=10)
# patient_uid_directories = rospy.Publisher('web/patient_uid/dir', String, queue_size=10)
# rospy.init_node('web_logger', anonymous=False)
# create_directories()

dir = expanduser("~") + '/Desktop/cabinet_db/'

def create_uid_directories(num, _time):
#    time = datetime.datetime.today().strftime('%Y-%m-%d_%H:%M:%S')

    if not os.path.exists(dir + '%s'%num ):
        os.makedirs(dir + '%s'%num )

    if not os.path.exists(dir + '%s'%num + '/' + _time):
        os.makedirs(dir + '%s'%num + '/' + _time)
    return str(dir + '%s'%num + '/' + _time)


def create_patient_directory():
    pass



from threading import Timer

class UserProfileList(  mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.generics.GenericAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.person_serializer

    def get_authenticators(self):
        if self.request.method == "POST":
            return []
        else: return [PersonAuthentication()]
        return super(UserProfileList, self).get_authenticators()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user:
            return HttpResponse(json.dumps(self.serializer_class(instance = request.user).data), status=200,
                                content_type='application/json; charset=utf8')
        else:
            return HttpResponse(json.dumps({'errors': 'اول با حساب خود وارد شوید'}), status=400,
                                content_type='application/json; charset=utf8')

    def put(self, request, *args, **kwargs):
        if request.user :
            s = self.serializer_class(instance=request.user,partial=True,data=request.data)
            if s.is_valid():
                s.save()
            return HttpResponse(json.dumps(self.serializer_class(request.user).data), status=200,
                                content_type='application/json; charset=utf8')
        else:
            return HttpResponse(json.dumps({'errors': 'اول با حساب خود وارد شوید'}), status=400,
                                content_type='application/json; charset=utf8')

class SessionView(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    permission_classes = (IsLogin,)

    @list_route(methods=['get'],permission_classes=[NotStarted]) #auth
    def start(self,request):       
        session = request.user.start_session()
        ros.patient_uid.publish(str(request.user.id))
        ros.patient_uid_directories.publish('%s'%create_uid_directories(str(request.user.id), str(session.start_time)))

        return HttpResponse(json.dumps({'starttime': session.stage.start_time, 'duration': session.stage.duration}), status=200,
                            content_type='application/json; charset=utf8')
    
    @list_route(methods=['get'],permission_classes=[StartedSession]) #auth
    def stop(self,request):                         
        request.user.end_session()
        return HttpResponse("", status=200,
                            content_type='application/json; charset=utf8')
                            
class StageView(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication, )
    permission_classes = (IsLogin, StartedSession, )
    serializer_class = serializer.stage_serializer

    @list_route(methods=['put']) #auth
    def autoupdate(self,request):

        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            status = data['autoupdate']
            session = request.user.current_session()
            session.stage.auto_update = status
            session.stage.save()
            return HttpResponse(json.dumps(""), status=200,
                                content_type='application/json; charset=utf8')

        except(ValueError, json.JSONDecodeError):
            return HttpResponse(json.dumps({'errors': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')

    @list_route(methods=['get']) #auth
    def status(self,request):                         
        stage = request.user.current_session().stage

        return HttpResponse(json.dumps(self.serializer_class(instance = stage).data), status=200,
                            content_type='application/json; charset=utf8')

class GameCommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    permission_classes = (IsLogin,)

    @list_route(methods=['get'],permission_classes=[NotStarted]) #auth
    def start(self,request):                         
        session = request.user.start_session()
        ros.patient_uid.publish(str(request.user.id))
        ros.patient_uid_directories.publish('%s'%create_uid_directories(str(request.user.id), str(session.start_time)))

        return HttpResponse(json.dumps({'starttime': session.stage.start_time, 'duration': session.stage.duration}), status=200,
                            content_type='application/json; charset=utf8')


 

    @list_route(methods=['post'], permission_classes=[StartedGame])  # auth
    def send_data(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            car = data['car']
            game = data['game']
            system = data['system']
            print(car,game,system)
            # TODO
            # do something with data            # do something with data

            return HttpResponse("", status=200,
                                content_type='application/json; charset=utf8')
        except (ValueError, json.JSONDecodeError):
            return HttpResponse(json.dumps({'errors': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')

class WheelCommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    permission_classes = (IsLogin,)


    @list_route(methods=['get'],permission_classes=[StartedGame, ManualStageUpdate]) #auth
    def start(self,request):
        request.user.change_stage(settings.WHEEL_STAGE)
        session = request.user.current_session()
        return HttpResponse(json.dumps({'starttime': session.stage.start_time, 'duration': session.stage.duration}), status=200,
                            content_type='application/json; charset=utf8')

    @list_route(methods=['post'], permission_classes=[StartedWheel])  # auth
    def perform(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            status = data['status']
            ros.wheel_status.publish(str(status))
            # TODO 
            return HttpResponse("", status=200,
                                content_type='application/json; charset=utf8')
        except(ValueError, json.JSONDecodeError):
            return HttpResponse(json.dumps({'errors': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')



class ParrotCommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    queryset = models.command.objects.all()
    serializer_class = serializer.command_serializer
    permission_classes = (IsLogin,)



    @list_route(methods=['get'],permission_classes=[StartedWheel, ManualStageUpdate]) #auth
    def start(self,request):
        request.user.change_stage(settings.PARROT_STAGE)
        session = request.user.current_session()
        return HttpResponse(json.dumps({'starttime': session.stage.start_time, 'duration': session.stage.duration}), status=200,
                            content_type='application/json; charset=utf8')

    @list_route(methods=['get'], permission_classes=[StartedParrot])  # auth
    def commands(self, request):
        ret = {}
        query = self.queryset.filter(tag="P_S1").order_by("priority", "arg")
        ret["Parrot Senario 1"] = self.serializer_class(instance=query, many=True).data
        query = self.queryset.filter(tag="P_S2").order_by("priority", "arg")
        ret["Parrot Senario 2"] = self.serializer_class(instance=query, many=True).data
        query = self.queryset.filter(tag="P_M").order_by("priority", "arg")
        ret["Parrot Movment"] = self.serializer_class(instance=query, many=True).data
        query = self.queryset.filter(tag="P_A").order_by("priority", "arg")
        ret["Parrot Auto"] = self.serializer_class(instance=query, many=True).data

        # print(ret)
        return HttpResponse(json.dumps(ret), status=200,
                            content_type='application/json; charset=utf8')


    @list_route(methods=['post'], permission_classes=[StartedParrot, ManualStageUpdate])  # auth
    def perform(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            commandID = data['commandID']
            command = self.queryset.get(pk=commandID)
            ros.parrot_command_name.publish(str(command.name))
            if (command.isVoice):
                ros.parrot_voice_commands.publish(command.voiceFile.path)
            else:
                ros.parrot_command.publish(str(command.arg))
            # TODO 
            # do something with data
            return HttpResponse("", status=200,
                                content_type='application/json; charset=utf8')
        except (ValueError, json.JSONDecodeError):
            return HttpResponse(json.dumps({'errors': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')

    @list_route(methods=['get'], permission_classes=[StartedParrot, ManualStageUpdate])  # auth
    def stop(self, request):
        request.user.change_stage(settings.DONE_STAGE)
        request.user.end_session()
        return HttpResponse(json.dumps(""), status=200,
                            content_type='application/json; charset=utf8')

class ToyCarData(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.generics.GenericAPIView):
    queryset = models.ToyCar.objects.all()
    serializer_class = serializer.toycar_serializer
    permission_classes = (AnyActiveSessions, AnyAtGameStage)
    authentication_classes = ()

        
    def perform_create(self, serializer):
        user_session = models.Patient.objects.get(login_status= True).current_session()
        serializer.save(session= user_session)
        
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except IntegrityError: 
                return HttpResponse(json.dumps({'errors': 'Data for this timestamp were already sent'}), status=400,
                                content_type='application/json; charset=utf8')


    
#####           __________________________________________  AUTH _____________________________________________


from .models import Patient
from rest_framework import authentication
from rest_framework import exceptions
from .token import decodeToken,generateToken
from time import time
import json
import codecs
from django.http import HttpResponse
from AILab.settings import AUTH_TIME_DELTA as timeDelta
from website.serializer import person_serializer
from django.views.decorators.csrf import csrf_exempt
from .authentication import decode_and_check_auth_token

@csrf_exempt
def obtain_token(request):
    try:
        data=json.loads(codecs.decode(request.body,'utf-8'))
        personID = data['personID']
    except (ValueError, json.JSONDecodeError):
        return HttpResponse(json.dumps({'errors': 'ورودی نادرست'}), status=400,
                            content_type='application/json; charset=utf8')

    try:
        user = Patient.objects.get(personID = personID)
    except Patient.DoesNotExist:
        return HttpResponse(json.dumps({"errors":"کاربری با این مشخصات وجود ندارد"}), status=401, content_type='application/json; charset=utf8')

    try:
        login_person = Patient.objects.get(login_status=True , last_activity__gt=time()-timeDelta)
        if not (login_person.personID == personID):
            return HttpResponse(json.dumps({'errors': 'فرد دیگری وارد شده است'}), status=400,
                                content_type='application/json; charset=utf8')
    except Patient.DoesNotExist:
        pass

    data={'id': user.id}
    
    for another_user in Patient.objects.filter(login_status=True):
        another_user.login_status=False
        another_user.save()

    token = generateToken(data)
    user.last_activity = time()    
    user.login_status = True
    user.save()
    if user.check_session():
        user.resume_session()
    # patient_uid.publish(str(user.id))
    # patient_uid_directories.publish('%s'%create_uid_directories(str(user.id)))

    return HttpResponse(json.dumps({'token': token, 'id':user.id}), status=200,
                    content_type='application/json; charset=utf8')


@csrf_exempt
def verify_token(request):
    try:
        user = PersonAuthentication.authenticate(None, request)[0]
        user.last_activity = time()
        user.save()
        return HttpResponse(status=200, content_type='application/json; charset=utf8')
    
    except exceptions.AuthenticationFailed as e: 
        return HttpResponse(json.dumps({"errors": str(e)}), status=400, content_type='application/json; charset=utf8')


@csrf_exempt
def remove_token(request):
    try:
        user = PersonAuthentication.authenticate(None, request)[0]
        user.login_status = False
        user.last_activity = time()
        user.save()
        if user.check_session():
            user.pause_session()
        return HttpResponse(json.dumps({"message": "logout complete"}), status=200,
                            content_type='application/json; charset=utf8')

    except exceptions.AuthenticationFailed as e:
        return HttpResponse(json.dumps({"errors":"کاربری با این مشخصات وارد نشده"}), status=400, content_type='application/json; charset=utf8')


def index(request,path):
    with open("./index.html") as index_file:
        return HttpResponse(index_file,status=200)