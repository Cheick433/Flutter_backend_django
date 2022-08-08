from django.urls import path

from api import views
from . import views
from rest_framework import routers
from .views import HistoryCourseViewSet, SignUpView, TripView, UserViewset


router = routers.DefaultRouter()
router.register('users', UserViewset)
urlpatterns = [
    path('trip/', TripView.as_view({'get': 'list'}), name='trip_list'),
    path('<uuid:trip_id>/', TripView.as_view({'get': 'retrieve'}), name='trip_detail'),
    path('historyCourse/', HistoryCourseViewSet.as_view({'get': 'list'}), name='DriverCourse'),
    
    

]

urlpatterns = urlpatterns + router.urls
