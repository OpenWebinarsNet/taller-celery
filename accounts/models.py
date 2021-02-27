from django.db import models

# Create your models here.
from django.db.models import FloatField, CharField, DateTimeField, ForeignKey, CASCADE, EmailField


class Account(models.Model):
    owner = EmailField()
    amount = FloatField()


class Notification(models.Model):
    recipient_email = EmailField()
    text = CharField(max_length=500)
    created_at = DateTimeField(auto_now_add=True)


class TransferStates(models.TextChoices):
    IN_PROGRESS = 'IN PROGRESS'
    ERROR = 'ERROR'
    FINISHED = 'FINISHED'


class Transfer(models.Model):
    amount = FloatField()
    origin_account = ForeignKey(Account, on_delete=CASCADE, related_name='origin_account')
    destination_account = ForeignKey(Account, on_delete=CASCADE, related_name='destination_account')
    status = CharField(max_length=20, choices=TransferStates.choices, default=TransferStates.IN_PROGRESS)
    created_at = DateTimeField(auto_now_add=True)
    finished = DateTimeField(null=True)


