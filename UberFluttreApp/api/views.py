from curses import A_PROTECT
from re import A
import statistics
from telnetlib import STATUS
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
import datetime
from Users import serializers

from api.models import Course, Driver
#from Course import STATUSES
from .serializers import LogInDriverSerializer, NestedTripSerializer, DriverSerializer, TripSerializer



# Create your views here.
class SignUpDriverView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = DriverSerializer
    


class LogInDriverView(TokenObtainPairView):
    serializer_class = LogInDriverSerializer

class CourseList(generics.ListCreateAPIView):
    #queryset = course = Course.objects.filter(created=datetime.datetime.now())
    queryset = course = Course.objects.all()
    serializer_class = NestedTripSerializer


################# cREATION ET AFFICHAGE LES DONNEES DU COURSE  #######################

class List_Courses(generics.ListCreateAPIView):     
    queryset = Course.objects.all()
    serializer_class = NestedTripSerializer   


##################  Recuperation les donnees d;uun course  ############################      

class CourseDetails(generics.RetrieveDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = NestedTripSerializer
    lookup_field ='pk'



class TripDriverView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = NestedTripSerializer(queryset)

    def get_queryset(self):
        user = self.request.user
        #if user.group == 'Driver':
        return Course.objects.filter(Q(status=Course.REQUESTED) | Q(driver=user))
        #if user.group == 'User':
        #return Course.objects.filter(rider=user)
        #return Course.objects.none()
    

# @api_view(['GET','PUL'])
# def accepterCourse(self, request, pk):
#     course = Course.objects.get(pk=pk)
#     course.STATUS = 'STARTED'
#     course.driver = self.request.user
#     return Response(course)

#def annulerCourse(self,request, ):

#def ArreterCourse(self, request, pk):
#   course=Course.objects.get(pk = pk)


######################### MANIPULATION LES DONNEES DU COURSE ###########################

class CourseAPIView(APIView):
    def get(self, request):
        course = Course.objects.all()
        data = NestedTripSerializer(course, many=True).data
        return Response(data)
    def post(self, request):
        serializer = NestedTripSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=STATUS.HTTP_201_CREATED)
        return Response(serializer.errors, status=STATUS.HTTP_400_BAD_REQUEST)
class Course_pk(APIView):

    def get_object(self, pk):
        try:

            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:

            raise Http404    
    def get(self, request, pk):

        course = self.get_object(pk)
        serializer = NestedTripSerializer(course)
        return Response(serializer.data)
    def put(self, request, pk):
        course=self.get_object(pk)
        serializer=NestedTripSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=STATUS.HTTP_404_BAD_REQUEST)  

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=STATUS.HTTP_204_NO_CONTENT)      

############  Manipulation de Driver  ############################################

class Driver_pk(APIView):

    def get_object(self, pk):
        try:

            return Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:

            raise Http404    
    def get(self, request, pk):

        driver = self.get_object(pk)
        serializer = DriverSerializer(driver)
        return Response(serializer.data)
    def put(self, request, pk):
        driver=self.get_object(pk)
        serializer=DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=STATUS.HTTP_404_BAD_REQUEST)  

    def delete(self, request, pk):
        rider = self.get_object(pk)
        rider.delete()
        return Response(status=STATUS.HTTP_204_NO_CONTENT)

    ##############################MANIPULATION PAR VIEWS SET ##################
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = NestedTripSerializer

    #authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def list(self, request):
        queryset = Course.objects.filter(status = 'STARTED')
        serializer = NestedTripSerializer(queryset, many=True)
        return Response(serializer.data)
    def update(self, request, pk):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk) 
        serializer = NestedTripSerializer(instance=course, data=request.data) 
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)    


class CourseDriverViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = Course.objects.filter(status = 'REQUESTED')
        serializer = NestedTripSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk) 
        serializer = NestedTripSerializer(instance=course, data=request.data) 
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    # def retrieve(self, request, pk=None):
    #     queryset = Course.objects.all()
    #     course = get_object_or_404(queryset, pk=pk)
    #     mastatus = 'STARTED'
    #     serializer = NestedTripSerializer(course,data={'status':mastatus})
    #     if serializer.is_valid:
    #         serializer.save()
    #     return Response(serializer.data)





@api_view(['GET','PUL'])
def accepterCourse(self, request, pk):
    course = Course.get_object_or_404(pk=pk)
    mastatus = 'STARTED'
    serializer = NestedTripSerializer(instance=course, data={'status':mastatus})
    if serializer.is_valid():
        serializer.save()
    
    #return Response(serializer.data, headers='Application/json')        