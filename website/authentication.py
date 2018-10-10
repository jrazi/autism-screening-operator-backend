
from .models import person
from rest_framework import authentication
from rest_framework import exceptions
from .token import decodeToken,generateToken
from time import time
import json
from django.http import HttpResponse


timeDelta = 15*60

class PersonAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTH')
        if token == None :
            return None

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


def obtain_token(request):
    try:
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        phone_number = request.data['phone_number']
        user = person.objects.get(first_name=first_name, last_name=last_name,
                              phone_number=phone_number)
    except:
        return HttpResponse(json.dumps({'errors': 'bad input'}), status=400,
                            content_type='application/json; charset=utf8')

    if (len(person.objects.filter(login_status=True , last_activity__gt=time()-timeDelta))):
        return HttpResponse(json.dumps({'errors': 'another user loged in'}), status=400,
                            content_type='application/json; charset=utf8')
    else:
        data={'first_name':first_name,'last_name':last_name,'phone_number':phone_number}
        token = generateToken(data)
        user.login_status=True
        user.last_activity=time()
        user.save()
        for another_user in person.objects.filter(login_status=True):
            another_user.login_status=False
            another_user.save()

        return HttpResponse(json.dumps({'token': token}), status=200,
                        content_type='application/json; charset=utf8')

def verify_token(request):
    try:
        token = request.data['token']
        data = decode_and_check_auth_token(token)
        user=person.objects.get(first_name=data['first_name'], last_name=data['last_name'],
                           phone_number=data['phone_number'])
    except:
        return HttpResponse(status=400,content_type='application/json; charset=utf8')
    if user.login_status==True and user.last_activity+timeDelta>time():
        return HttpResponse(status=200, content_type='application/json; charset=utf8')
    else:
        if user.login_status==True:
            user.login_status=False
            user.save()
        return HttpResponse(status=400,content_type='application/json; charset=utf8')


