from rest_framework import permissions
from time import time
from AILab.settings import AUTH_TIME_DELTA as timeDelta


class IsLogin(permissions.BasePermission):
    message = 'you\'re not Authenticate'

    def has_permission(self, request, view):

        if (request.user.last_activity+timeDelta > time() and request.user.login_status==True):
            return True

        return False

    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)