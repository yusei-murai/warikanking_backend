from django.contrib import admin
from user.models import User
from event.models import Event
from pay.models import Pay
from pay_result.models import PayResult

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(User,UserAdmin)
admin.site.register(Event)
admin.site.register(Pay)
admin.site.register(PayResult)