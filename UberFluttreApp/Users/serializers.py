from dataclasses import fields
import dataclasses

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueTogetherValidator
from api.models import Course, Driver, Rider, User


# class UserSerializer(serializers.ModelSerializer):
#     password1 = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)
#     group = serializers.CharField()

#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError('Passwords must match.')
#         return data

#     def create(self, validated_data):
#         group_data = validated_data.pop('group')
#         group, _ = Group.objects.get_or_create(name=group_data)
#         data = {key: value for key, value in validated_data.items() if key not in ('password1', 'password2')}
#         data['password'] = validated_data['password1']
#         user = self.Meta.model.objects.create_user(**data)
#         _,token = Token.objects.create(user = user)
#         token.save()        
#         user.groups.add(group)
#         user.save()
#         return token

#     class Meta:
#         model = get_user_model()
#         fields = (
#             'id',
#             'username',
#             'password1',
#             'password2',
#             'first_name',
#             'last_name',
#             'group',
#             #'photo',
#         )
#         read_only_fields = ('id',)

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        _,token = Token.objects.get_or_create(user = user)
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

class LogInSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
        )


class NestedTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        depth = 1
################serializer pour le driver############################################
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

####################  Serializer pour le Rider ########################################

class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = '__all__'        