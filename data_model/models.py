import uuid
from django.db import models
from user.models import User
from django.utils import timezone
import datetime

class Event(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField("イベント名", max_length=255,null=False)
    users = models.ManyToManyField("user.User")
    created_at = models.DateTimeField(null=False,default=datetime.datetime.now())

    def __str__(self):
        return self.name
    
class Adjustment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    event = models.ForeignKey("Event",on_delete=models.CASCADE,default=1,null=False)
    adjust_user = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1,related_name='pay_user',null=False)
    adjusted_user = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1,related_name='paid_user',null=False)
    amount_pay = models.IntegerField("支払い金額",default=0,null=False)
    created_at = models.DateTimeField(null=False,default=datetime.datetime.now())

    def __str__(self):
        return str(self.event) + " " + str(self.adjust_user) + " " + str(self.adjusted_user)
    
class Pay(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField("支払い名", max_length=255,null=False)
    event = models.ForeignKey("Event",on_delete=models.CASCADE,default=1)
    user = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1)
    amount_pay = models.IntegerField("支払い金額",default=0,null=False)
    created_at = models.DateTimeField(null=False,default=datetime.datetime.now())

    def __str__(self):
        return self.name
    
class PayRelatedUser(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    pay = models.ForeignKey("Pay",on_delete=models.CASCADE,default=1)
    user = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(null=False,default=datetime.datetime.now())

    def __str__(self):
        return str(self.pay.name) + "-" + str(self.user.name)
    
class Friend(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user_1 = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1,related_name='user1',null=False)
    user_2 = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1,related_name='user2',null=False)
    approval = models.BooleanField("承認",default=False,null=False)
    created_at = models.DateTimeField(null=False,default=datetime.datetime.now())

    def __str__(self):
        return str(self.user_1.name) + "-" + str(self.user_2.name)