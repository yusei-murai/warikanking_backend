import uuid
from django.db import models
from event.models import Event
from django.utils import timezone

class Pay(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField("支払い名", max_length=255,null=False)
    event = models.ForeignKey("event.Event",on_delete=models.CASCADE,default=1)
    user = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1)
    amount_pay = models.IntegerField("支払い金額",default=0,null=False)

    def __str__(self):
        return self.name