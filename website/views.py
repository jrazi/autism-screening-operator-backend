
#!/usr/bin/env python
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route,detail_route
from website import serializer,models
from website.permissions import IsLogin
import json
from django.http import HttpResponse

import rospy
from std_msgs.msg import String

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



# pub = rospy.Publisher('web/parrot',String,queue_size=10)
# rospy.init_node('webhandler',anonymous = False)

parrot_command_name = rospy.Publisher('web/parrot_command_name', String, queue_size=10)
parrot_command = rospy.Publisher('web/parrot_commands', String, queue_size=10)
parrot_voice_commands = rospy.Publisher('web/parrot_voice_commands', String, queue_size=10)
patient_uid = rospy.Publisher('web/patient_uid', String, queue_size=10)
patient_uid_directories = rospy.Publisher('web/patient_uid/dir', String, queue_size=10)
rospy.init_node('web_logger', anonymous=False)
create_directories()



def create_patient_directory():
    pass





class UserProfile(viewsets.GenericViewSet):

    queryset = models.person.objects.all()
    serializer_class = serializer.person_serializer

    def create(self,request):
        s = self.serializer_class(data=request.data)
        if s.is_valid():
            s.save()
            return HttpResponse(json.dumps(request.data), status=200, content_type='application/json; charset=utf8')
        else:
            return HttpResponse(json.dumps(s.errors), status=400, content_type='application/json; charset=utf8')

    @list_route(methods=['put','patch'],permission_classes=[IsLogin])  #auth
    def change(self,request):
        s = self.serializer_class(instance=request.user, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return HttpResponse(json.dumps({'message': 'update succesfully'}), status=200,
                                content_type='application/json; charset=utf8')
        else:
            return HttpResponse(json.dumps(s.errors), status=400, content_type='application/json; charset=utf8')

class Commands(viewsets.GenericViewSet):
    queryset = models.command.objects.all()
    serializer_class = serializer.command_serializer
    permission_classes = (IsLogin,)

    @list_route(methods=['get'],permission_classes=[IsLogin]) #auth
    def weel(self,requset):
        query=self.queryset.filter(tag="W").order_by("priority","arg")
        s = self.serializer_class(instance=query,many=True)
        return HttpResponse(json.dumps(s.data), status=200,
                            content_type='application/json; charset=utf8')

    @list_route(methods=['get'],permission_classes=[IsLogin]) #auth
    def parrot(self,request):
        ret = {}
        query = self.queryset.filter(tag="P_S1").order_by("priority","arg")
        ret["Parrot Senario 1"] = self.serializer_class(instance=query, many=True).data
        query = self.queryset.filter(tag="P_S2").order_by("priority","arg")
        ret["Parrot Senario 2"] = self.serializer_class(instance=query, many=True).data
        query = self.queryset.filter(tag="P_M").order_by("priority","arg")
        ret["Parrot Movment"] = self.serializer_class(instance=query, many=True).data

        #print(ret)
        return HttpResponse(json.dumps(ret), status=200,
                            content_type='application/json; charset=utf8')


    @detail_route(methods=['get'],permission_classes=[IsLogin]) #auth
    def perform(self,request,pk=None):
        obj = self.queryset.get(pk=pk)

        parrot_command_name.publish(str(obj.name))
        if(obj.isVoice):
            # pub.publish("command:"+str(obj.arg)+"#"+obj.voiceFile.path)
            parrot_voice_commands.publish(obj.voiceFile.path)
            print(obj.voiceFile.path)
        else :
            # pub.publish("command:"+str(obj.arg))
            parrot_command.publish(str(obj.arg))
        # do some thing with the code
        return HttpResponse(status=200,
                            content_type='application/json; charset=utf8')




#####           __________________________________________  AUTH _____________________________________________


from .models import person
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
        first_name = data['first_name']
        last_name = data['last_name']
        phone_number = data['phone_number']
    except:
        return HttpResponse(json.dumps({'errors': 'bad input'}), status=400,
                            content_type='application/json; charset=utf8')

    try:
        login_person = person.objects.get(login_status=True , last_activity__gt=time()-timeDelta)
    except:
        pass
    else:
        if not (login_person.first_name==first_name and login_person.last_name==last_name and login_person.phone_number==phone_number):
            return HttpResponse(json.dumps({'errors': 'another user loged in'}), status=400,
                                content_type='application/json; charset=utf8')

    try:
        user = person.objects.get(first_name=first_name, last_name=last_name,
                                  phone_number=phone_number)
    except:

        return HttpResponse(json.dumps({"errors":"user not exist"}), status=401, content_type='application/json; charset=utf8')



    data={'first_name':first_name,'last_name':last_name,'phone_number':phone_number}
    for another_user in person.objects.filter(login_status=True):
        another_user.login_status=False
        another_user.save()

    token = generateToken(data)
    user.login_status = True
    user.last_activity = time()
    user.save()
    # pub.publish("login:"+str(user.id))
    patient_uid.publish(str(user.id))
    patient_uid_directories.publish('%s'%create_uid_directories(str(user.id)))

    return HttpResponse(json.dumps({'token': token}), status=200,
                    content_type='application/json; charset=utf8')


@csrf_exempt
def verify_token(request):
    try:
        token = json.loads(codecs.decode(request.body,'utf-8'))['token']
        data = decode_and_check_auth_token(token)
        user=person.objects.get(first_name=data['first_name'], last_name=data['last_name'],
                           phone_number=data['phone_number'])
    except:
        return HttpResponse(status=400,content_type='application/json; charset=utf8')
    if user.login_status==True and user.last_activity+timeDelta>time():
        user.last_activity = time()
        user.save()
        return HttpResponse(status=200, content_type='application/json; charset=utf8')
    else:
        if user.login_status==True:
            user.login_status=False
            user.save()
        return HttpResponse(status=400,content_type='application/json; charset=utf8')


@csrf_exempt
def remove_token(request):
    try:
        token = json.loads(codecs.decode(request.body,'utf-8'))['token']
        data = decode_and_check_auth_token(token)
        user=person.objects.get(first_name=data['first_name'], last_name=data['last_name'],
                           phone_number=data['phone_number'])
    except:
        return HttpResponse(status=400,content_type='application/json; charset=utf8')


    user.login_status=False;
    user.last_activity = time()
    user.save()
    return HttpResponse(json.dumps({"message":"logout complete"}),status=200, content_type='application/json; charset=utf8')
