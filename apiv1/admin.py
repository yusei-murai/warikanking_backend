from django.contrib import admin
from user.models import User
from event.models import Event
from pay.models import Pay

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Pay)

# Register your models here.
