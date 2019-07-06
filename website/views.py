
#!/usr/bin/env python
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route,detail_route
from website import serializer,models
from website.permissions import *
from website.authentication import PersonAuthentication
from rest_framework import mixins
import json
from django.http import HttpResponse

import os
from os.path import expanduser
import datetime





dir = expanduser("~") + '/Desktop/'
def create_directories():
    global dir
    if not os.path.exists(dir + 'cabinet_db'):
        os.makedirs(dir + 'cabinet_db')
    dir = dir + 'cabinet_db/'


def create_uid_directories(num):
    time = datetime.datetime.today().strftime('%Y-%m-%d_%H:%M:%S')

    if not os.path.exists(dir + '%s'%num ):
        os.makedirs(dir + '%s'%num )

    if not os.path.exists(dir + '%s'%num + '/' + time):
        os.makedirs(dir + '%s'%num + '/' + time)
    print (dir + '%s'%num + '/' + time)
    return str(dir + '%s'%num + '/' + time)


# import rospy
# from std_msgs.msg import String

# parrot_command_name = rospy.Publisher('web/parrot_command_name', String, queue_size=10)
# parrot_command = rospy.Publisher('web/parrot_commands', String, queue_size=10)
# parrot_voice_commands = rospy.Publisher('web/parrot_voice_commands', String, queue_size=10)
# patient_uid = rospy.Publisher('web/patient_uid', String, queue_size=10)
# patient_uid_directories = rospy.Publisher('web/patient_uid/dir', String, queue_size=10)
# rospy.init_node('web_logger', anonymous=False)
# create_directories()



def create_patient_directory():
    pass



class UserProfileList(  mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.generics.GenericAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.person_serializer
    authentication_classes = (PersonAuthentication,)

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

class PreGameCommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    permission_classes = (IsLogin,)

    @list_route(methods=['get'],permission_classes=[NotStarted]) #auth
    def start(self,request):
        request.user.stage = "PG"
        request.user.save()
        return HttpResponse("", status=200,
                            content_type='application/json; charset=utf8')

    @list_route(methods=['post'], permission_classes=[StartedPreGame])  # auth
    def send_data(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            car = data['car']
            game = data['game']
            system = data['system']
            print(car,game,system)
            # do something with data
            return HttpResponse("", status=200,
                                content_type='application/json; charset=utf8')
        except:
            return HttpResponse(json.dumps({'errors': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')

class WeelCommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    permission_classes = (IsLogin,)



    @list_route(methods=['get'],permission_classes=[StartedPreGame]) #auth
    def start(self,request):
        request.user.stage = "W"
        request.user.save()
        return HttpResponse(json.dumps(""), status=200,
                            content_type='application/json; charset=utf8')

    @list_route(methods=['post'], permission_classes=[StartedWeel])  # auth
    def perform(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            status = data['status']
            print(status)
            # do something with data
            return HttpResponse("", status=200,
                                content_type='application/json; charset=utf8')
        except:
            return HttpResponse(json.dumps({'errors': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')



class ParrotCommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    queryset = models.command.objects.all()
    serializer_class = serializer.command_serializer
    permission_classes = (IsLogin,)



    @list_route(methods=['get'],permission_classes=[StartedWeel]) #auth
    def start(self,request):
        request.user.stage = "P"
        request.user.save()
        return HttpResponse(json.dumps(""), status=200,
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


    @list_route(methods=['post'], permission_classes=[StartedParrot])  # auth
    def perform(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            commandID = data['commandID']
            command = self.queryset.get(pk=commandID)
            # parrot_command_name.publish(str(command.name))
            if (command.isVoice):
                # parrot_voice_commands.publish(command.voiceFile.path)
                print(command.voiceFile.path)
            else:
                # parrot_command.publish(str(command.arg))
                print(command.arg)
            # do something with data
            return HttpResponse("", status=200,
                                content_type='application/json; charset=utf8')
        except:
            return HttpResponse(json.dumps({'errors': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')

    @list_route(methods=['get'], permission_classes=[StartedParrot])  # auth
    def stop(self, request):
        request.user.stage = "D"
        request.user.save()
        return HttpResponse(json.dumps(""), status=200,
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
    except:
        return HttpResponse(json.dumps({'errors': 'ورودی نادرست'}), status=400,
                            content_type='application/json; charset=utf8')

    try:
        login_person = Patient.objects.get(login_status=True , last_activity__gt=time()-timeDelta)
    except:
        pass
    else:
        if not (login_person.personID== personID):
            return HttpResponse(json.dumps({'errors': 'فرد دیگری وارد شده است'}), status=400,
                                content_type='application/json; charset=utf8')

    try:
        user = Patient.objects.get(personID = personID)
    except:

        return HttpResponse(json.dumps({"errors":"اطلاعات درست نیست"}), status=401, content_type='application/json; charset=utf8')



    data={'id': user.id}
    for another_user in Patient.objects.filter(login_status=True):
        another_user.login_status=False
        another_user.save()

    token = generateToken(data)
    user.login_status = True
    user.last_activity = time()
    user.stage = "NS"
    user.save()
    # patient_uid.publish(str(user.id))
    # patient_uid_directories.publish('%s'%create_uid_directories(str(user.id)))

    return HttpResponse(json.dumps({'token': token, 'id':user.id}), status=200,
                    content_type='application/json; charset=utf8')


@csrf_exempt
def verify_token(request):
    try:
        token = json.loads(codecs.decode(request.body, 'utf-8'))['token']
        data = decode_and_check_auth_token(token)
        user = Patient.objects.get(id = data['id'])
    except:
        return HttpResponse(status=400, content_type='application/json; charset=utf8')
    if user.login_status == True and user.last_activity + timeDelta > time():
        user.last_activity = time()
        user.save()
        return HttpResponse(status=200, content_type='application/json; charset=utf8')
    else:
        if user.login_status == True:
            user.login_status = False
            user.save()
        return HttpResponse(status=400, content_type='application/json; charset=utf8')




@csrf_exempt
def remove_token(request):
    try:
        token = json.loads(codecs.decode(request.body, 'utf-8'))['token']
        data = decode_and_check_auth_token(token)
        user = Patient.objects.get(id = data['id'])
        user.login_status = False
        user.last_activity = time()
        user.stage = "NS"
        user.save()
        return HttpResponse(json.dumps({"message": "logout complete"}), status=200,
                            content_type='application/json; charset=utf8')
    except:
        return HttpResponse(status=400, content_type='application/json; charset=utf8')


def index(request,path):
    with open("./index.html") as index_file:
        return HttpResponse(index_file,status=200)




