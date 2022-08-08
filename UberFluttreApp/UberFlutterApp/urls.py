"""UberFlutterApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import Users
from Users.views import LogInView, SignUpView
import api
import Users
from Users import urls
from api import urls
from api import views
from api.views import Course_pk, accepterCourse
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from rest_framework.routers import DefaultRouter

admin.autodiscover()



router = DefaultRouter()
router.register('Course',views.CourseViewSet, basename='Course')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rider/', include(Users.urls)),
    path('api/', include(api.urls)),
     path('api/sign_up/', SignUpView.as_view(), name='sign_up'),
     #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('api/course/<int:pk>/', Course_pk.as_view(), name='Course_pk'),
     path('token/refresh/', LogInView.as_view(), name='token_refresh'),
      path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    

     
]
urlpatterns = urlpatterns + router.urls