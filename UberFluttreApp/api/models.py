from asyncio.windows_events import NULL
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse



# Create your models here.
#class User(models.Model):
#    Nom = models.CharField(max_length=30)
#    Prenom = models.CharField(max_length=30)
#    Email = models.CharField(max_length=30)
#    Date_naissance = 
#class User(AbstractUser):
   # is_Driver = models.BooleanField(default=False)
   # is_Rider = models.BooleanField(default=False)
###################################################################
class User(AbstractUser):
    #photo = models.ImageField(upload_to='photos', null=True, blank=True)
    #is_driver = models.BooleanField(default=False)
    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].name if groups else None

###########################Rider##################################

class Rider(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    Nom = models.CharField(max_length=30)
    Prenom = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    bio = models.CharField(max_length=60)
    #avatar = models.ImageField(upload_to='ProfilePicture/')
    current_location = models.ForeignKey('api.Location', related_name='current_location', on_delete=models.CASCADE, null=True)
    contact_info = models.CharField(max_length=50)

    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].Nom if groups else None


        ########################################
class Driver(models.Model):
    driver = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    Nom = models.CharField(max_length=30)
    Prenom = models.CharField(max_length=30)
    cin = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    driver_location = models.JSONField(null=True, blank=True)
    status_occupement = models.BooleanField(default=False)

    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].Nom if groups else None


class Course(models.Model):
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    STATUSES = (
        (REQUESTED, REQUESTED),
        (STARTED, STARTED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
        (CANCELED, CANCELED),
    )

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lieu_depart = models.CharField(max_length=255)
    lieu_arrive = models.CharField(max_length=255, default=NULL)
    #lieu = models.OneToOneField('Location', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=STATUSES, default=REQUESTED)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='trips_as_driver'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='course_as_rider'
    )
    driver_location = models.JSONField(null=True, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)


class Location(models.Model):
#Attribute Variables for Location class to represent different columns in database
    longitude = models.CharField(max_length=10)
    latitude = models.CharField(max_length=10)
    location_name = models.CharField(max_length=20)

    '''Method to filter database results'''
   # def __str__(self):
       # return self.location_name


##class car###########################################################################
class Car(models.Model):
#Attribute Variables for Car class to represent different columns in database
    '''
    car_brand -: This is the car brand driven by driver for easy identification 
    number_plate-: Vehicle registration number for more accurate identification
    seat_number-: This are the number of seats available in drivers car
    '''
    car_model = models.CharField(max_length=50)
    numero_plate = models.CharField(max_length=20)
    seat_number = models.CharField(max_length=20)

    '''Method to filter database results'''
    def __str__(self):
        return self.car_model





