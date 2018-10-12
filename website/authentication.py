
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



class PersonAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTH')
        if token == None :
            return (None,None)

        try :
            data = decode_and_check_auth_token(token)
        except:
            raise exceptions.AuthenticationFailed('bad token')
        try:
            user = person.objects.get(first_name=data['first_name'],last_name=data['last_name'],phone_number=data['phone_number'])
        except:
            raise exceptions.AuthenticationFailed('No such user')

        if user.last_activity+timeDelta < time() or user.login_status==False:
            if user.login_status==True:
                user.login_status=False
                user.save()
            raise exceptions.AuthenticationFailed('not logined')

        else:
            user.last_activity=time()
            user.save()
            return (user, None)


def decode_and_check_auth_token(token):
    data = decodeToken(token)
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = data['phone_number']
    return data

from django.views.decorators.csrf import csrf_exempt

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
        user = person.objects.get(first_name=first_name, last_name=last_name,
                                  phone_number=phone_number)
    except:
        s = person_serializer(data=request.data)
        if s.is_valid():
            s.save()
            user = person.objects.get(first_name=first_name, last_name=last_name,
                                      phone_number=phone_number)
        else:
            return HttpResponse(json.dumps(s.errors), status=400, content_type='application/json; charset=utf8')


    if (len(person.objects.filter(login_status=True , last_activity__gt=time()-timeDelta))):
        return HttpResponse(json.dumps({'errors': 'another user loged in'}), status=400,
                            content_type='application/json; charset=utf8')
    else:
        data={'first_name':first_name,'last_name':last_name,'phone_number':phone_number}
        for another_user in person.objects.filter(login_status=True):
            another_user.login_status=False
            another_user.save()

        token = generateToken(data)
        user.login_status = True
        user.last_activity = time()
        user.save()

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