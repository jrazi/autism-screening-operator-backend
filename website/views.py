
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route,detail_route
from website import serializer,models
from website.permissions import IsLogin
from time import time
from datetime import datetime
from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse
from itertools import chain


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
        query=self.queryset.filter(tag="W")
        s = self.serializer_class(instance=query,many=True)
        return HttpResponse(json.dumps(s.data), status=200,
                            content_type='application/json; charset=utf8')

    @list_route(methods=['get'],permission_classes=[IsLogin]) #auth
    def parrot(self,request):
        ret = {}
        query = self.queryset.filter(tag="P_S1")
        ret["Parrot Senario 1"] = self.serializer_class(instance=query, many=True).data
        query = self.queryset.filter(tag="P_S2")
        ret["Parrot Senario 2"] = self.serializer_class(instance=query, many=True).data
        query = self.queryset.filter(tag="P_M")
        ret["Parrot Movment"] = self.serializer_class(instance=query, many=True).data

        print(ret)
        return HttpResponse(json.dumps(ret), status=200,
                            content_type='application/json; charset=utf8')


    @detail_route(methods=['get'],permission_classes=[IsLogin]) #auth
    def perform(self,request,pk=None):
        obj = self.queryset.get(pk=pk)
        # do some thing with the code
        return HttpResponse(status=200,
                            content_type='application/json; charset=utf8')
