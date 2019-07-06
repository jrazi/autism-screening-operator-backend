from rest_framework import permissions
from time import time
from AILab.settings import AUTH_TIME_DELTA as timeDelta


class IsLogin(permissions.BasePermission):
    message = 'you\'re not Authenticate'

    def has_permission(self, request, view):

        if (request.user==None):
            return False
        if (request.user.last_activity+timeDelta > time() and request.user.login_status==True):
            return True

        return False

    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)



class NotStarted(permissions.BasePermission):
    message = 'you\'re can\'t start pregame at this stage'
    def has_permission(self, request, view):
        if (request.user==None):
            return False
        if (request.user.stage == "NS"):
            return True
        else:
            return False
    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)

class StartedPreGame(permissions.BasePermission):
    message = 'you\'re not started the pregame yet'
    def has_permission(self, request, view):
        if (request.user == None):
            return False
        if (request.user.stage == "PG"):
            return True
        else:
            return False
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class StartedWeel(permissions.BasePermission):
    message = 'you\'re not started Weel yet'

    def has_permission(self, request, view):
        if (request.user == None):
            return False
        if (request.user.stage == "W"):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class StartedParrot(permissions.BasePermission):
    message = 'you\'re not started parrot yet'

    def has_permission(self, request, view):
        if (request.user == None):
            return False
        if (request.user.stage == "P"):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)