from django.urls import path

from .views import Course_pk, CourseDriverViewSet, CourseList, List_Courses, TripDriverView, accepterCourse,CourseDetails
from api import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('RequestedCourse',views.CourseDriverViewSet, basename='RequestedCourse')
urlpatterns = [
    #path('', TripView.as_view({'get': 'list'}), name='trip_list'),
    #path('<uuid:trip_id>/', TripView.as_view({'get': 'retrieve'}), name='trip_detail'),
    path('list', views.List_Courses.as_view(), name='courses_list'),
    #path('', views.DriverDetails.as_view(), name='course_list'),
    path('trip', TripDriverView.as_view({'get': 'list'}), name='trip_list'),
    path('course/', views.Course_pk.as_view(), name='Courselist'),
    path('Course/<int:pk>/', views.accepterCourse, name='accepter'),
    path('CourseDetails/<int:pk>/', views.CourseDetails.as_view(), name='details'),
    path('CourseList/', views.CourseAPIView.as_view(), name='List'),


    #path('DriverCourse/', CourseDriverViewSet.as_view({'get': 'list'}), name='DriverCourse'),
    #path('api/DriverCourse/<int:pk>/', CourseDriverViewSet.as_view({'get': 'update'}), name='trip_detail'),
    
]
urlpatterns = urlpatterns + router.urls
