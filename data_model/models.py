import uuid
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Emailが必須です")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_identifier = models.CharField("ユーザID", max_length=255, unique=True, null=False, default=uuid.uuid4())
    email = models.EmailField("メールアドレス", max_length=255, unique=True)
    name = models.CharField("名前", max_length=255, unique=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name','user_identifier']

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("イベント名", max_length=255, null=False)
    users = models.ManyToManyField("User")
    created_at = models.DateTimeField(null=False)

    def __str__(self):
        return self.name


class Adjustment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, default=1, null=False)
    adjust_user = models.ForeignKey(
        "User", on_delete=models.CASCADE, default=1, related_name='pay_user', null=False)
    adjusted_user = models.ForeignKey(
        "User", on_delete=models.CASCADE, default=1, related_name='paid_user', null=False)
    amount_pay = models.IntegerField("支払い金額", default=0, null=False)
    created_at = models.DateTimeField(null=False)

    def __str__(self):
        return str(self.event) + " " + str(self.adjust_user) + " " + str(self.adjusted_user)


class Pay(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("支払い名", max_length=255, null=False)
    event = models.ForeignKey("Event", on_delete=models.CASCADE, default=1)
    user = models.ForeignKey("User", on_delete=models.CASCADE, default=1)
    amount_pay = models.IntegerField("支払い金額", default=0, null=False)
    created_at = models.DateTimeField(null=False)

    def __str__(self):
        return self.name


class PayRelatedUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pay = models.ForeignKey("Pay", on_delete=models.CASCADE, default=1)
    user = models.ForeignKey("User", on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(null=False)

    def __str__(self):
        return str(self.pay.name) + "-" + str(self.user.name)


class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_user = models.ForeignKey(
        "User", on_delete=models.CASCADE, default=1, related_name='request_user', null=False)
    requested_user = models.ForeignKey(
        "User", on_delete=models.CASCADE, default=1, related_name='requested_user', null=False)
    approval = models.BooleanField("承認", default=False, null=False)
    created_at = models.DateTimeField(null=False)
    
    class Meta:
        unique_together = ['request_user', 'requested_user']

    def __str__(self):
        return str(self.request_user.name) + "-" + str(self.requested_user.name)
