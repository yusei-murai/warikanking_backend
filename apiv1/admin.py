from django.contrib import admin
from user.models import User
from data_model.models import Pay, Adjustment, PayRelatedUser, Event, Friend

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(User,UserAdmin)
admin.site.register(Pay)
admin.site.register(Adjustment)
admin.site.register(PayRelatedUser)
admin.site.register(Event)
admin.site.register(Friend)