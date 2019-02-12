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
