import uuid
from django.db import models
from django.utils import timezone
import datetime

class Adjustment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    event = models.ForeignKey("event.Event",on_delete=models.CASCADE,default=1,null=False)
    adjust_user = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1,related_name='pay_user',null=False)
    adjusted_user = models.ForeignKey("user.User",on_delete=models.CASCADE,default=1,related_name='paid_user',null=False)
    amount_pay = models.IntegerField("支払い金額",default=0,null=False)
    created_at = models.DateTimeField(null=False,default=datetime.datetime.now().isoformat())

    def __str__(self):
        return str(self.event) + " " + str(self.adjust_user) + " " + str(self.adjusted_user)