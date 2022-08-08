from atexit import register
from django.contrib import admin

from api.models import Car, Course, Driver, Location, Rider, User

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Rider)
admin.site.register(Driver)
admin.site.register(Location)
admin.site.register(Car)