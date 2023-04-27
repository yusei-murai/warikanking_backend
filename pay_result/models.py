import uuid
from django.db import models
from event.models import Event
from django.utils import timezone

class PayResult(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    event = models.ForeignKey("event.Event",on_delete=models.CASCADE,default=1)
    pay_user = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1,related_name='pay_user')
    paid_user = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1,related_name='paid_user')
    amount_pay = models.IntegerField("支払い金額",default=0,null=False)

    def __str__(self):
        return self.id