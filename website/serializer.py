from rest_framework import serializers
from website import models


class command_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.command
        fields = ('id','name','performTime')
        read_only_fields = ('id','name','performTime')

class person_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient
        fields = ('first_name','last_name','phone_number','birthYear','gender','medicalInfo','personID')

class toycar_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.ToyCar
        fields = ('time', 'ac_x', 'ac_y', 'ac_z', 'encode1', 'encode2')

class stage_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stage
        fields = ('name', 'start_time', 'duration', 'auto_update')