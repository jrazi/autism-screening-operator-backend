from rest_framework import serializers
from website import models


class command_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.command
        fields = ('id','name')
        read_only_fields = ('id','name')

class person_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.person
        fields = ('first_name','last_name','phone_number','age')
        extra_kwargs = {'first_name': {'write_only': True},
                        'last_name': {'write_only': True},
                        'phone_number': {'write_only': True},
                        'age': {'write_only': True},}