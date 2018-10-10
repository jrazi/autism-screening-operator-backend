
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route,detail_route
from website import serializer,models
from rest_framework.permissions import IsAuthenticated
from time import time
from datetime import datetime
from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse
from itertools import chain


class UserProfile(viewsets.GenericViewSet):

    queryset = models.person.objects.all()
    serializer_class = serializer.person_serializer
    @list_route(methods=['post'])   #allowAny
    def create(self,request):
        pass
    @list_route(methods=['posst'])  #auth
    def change(self,request):
        pass

class Commands(viewsets.GenericViewSet):
    queryset = models.person.objects.all()
    serializer_class = serializer.command_serializer

    @list_route(methods=['get']) #auth
    def weel(self,requset):
        pass

    @list_route(methods=['get']) #auth
    def parrot(self,request):
        pass

    @detail_route(methods=['get']) #auth
    def perform(self,request,pk=None):
        pass