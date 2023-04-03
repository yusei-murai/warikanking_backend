import uuid
from django.db import models

class UserEvent(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    event_id = models.UUIDField("イベントID",null=False,editable=False)
    user_id = models.UUIDField("支払い者ID", null=False,editable=False)

    def __str__(self):
        return self.name