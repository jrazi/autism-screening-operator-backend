from rest_framework import permissions
from time import time
from AILab.settings import AUTH_TIME_DELTA as timeDelta


class IsLogin(permissions.BasePermission):
    message = 'Please login first'

    def has_permission(self, request, view):
        return request.user and request.user.last_activity+timeDelta > time() and request.user.login_status==True

    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)


class NotStarted(permissions.BasePermission):
    message = 'you can\'t start pregame at this stage'
    permission_classes = (IsLogin, )
    def has_permission(self, request, view):
        return request.user.stage == "NS"

    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)

class StartedPreGame(permissions.BasePermission):
    message = 'you\'re not started the pregame yet'
    permission_classes = (NotStarted, )
    def has_permission(self, request, view):
        return request.user.stage == "PG"

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class StartedWeel(permissions.BasePermission):
    message = 'you\'re not started Weel yet'
    permission_classes = (StartedPreGame, )
    def has_permission(self, request, view):
        return request.user.stage == "W"

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class StartedParrot(permissions.BasePermission):
    message = 'you\'re not started parrot yet'

    permission_classes = (StartedWeel, )
    def has_permission(self, request, view):
        return (request.user.stage == "P")

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)