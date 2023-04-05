import uuid
from django.db import models
from user.models import User

class Event(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField("イベント名", max_length=255,null=False)
    total = models.IntegerField("合計金額",default=0,null=False)
    number_people = models.IntegerField("合計金額",default=0,null=False)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title