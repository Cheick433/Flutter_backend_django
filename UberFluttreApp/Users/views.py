from contextvars import Token
from lib2to3.pgen2 import token
from telnetlib import STATUS
from urllib import response
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status

from api.models import Course, Driver,Rider, User
from .serializers import LogInSerializer, NestedTripSerializer, RiderSerializer, UserSerializer
from Users import serializers

from rest_framework.response import Response


class SignUpView(generics.CreateAPIView):
    # queryset = get_user_model().objects.all()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes= (AllowAny,)
    


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer
    authentication_classes = (BasicAuthentication,)


class TripView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = NestedTripSerializer(queryset)

    def get_queryset(self):
        user = self.request.user
        #if user.group == 'Driver':
           ## return Course.objects.filter(Q(status=Course.REQUESTED) | Q(driver=user))
        if user.group == 'user':
            return Course.objects.filter(rider=user)
        #return Course.objects.none()
########

#######################################  Manipulation le Rider##########################


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #authentication_classes = (AllowAny,)
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
        #_,token = Token.objects.get_or_create(user=serializer.instance)
            #serializer.create(validated_data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            # 'token': token.key,},
            # status= status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )    

    # def list(self, request, *args, **kwargs):

    #     response = {'message': 'you cant see that'}
    #     return Response(response)
    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)


class HistoryCourseViewSet(viewsets.ViewSet):
    queryset = Course.objects.all()
    serializer_class = NestedTripSerializer

    #authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = Course.objects.filter(status = 'STARTED')
        serializer = NestedTripSerializer(queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = Course.objects.all()
    #     course = get_object_or_404(queryset, pk=pk)
    #     serializer = NestedTripSerializer(course, data=)
    #     return Response(serializer.data)