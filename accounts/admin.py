from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from accounts.models import Account, Transfer, Notification


@admin.register(Account)
class AccountAdmin(ModelAdmin):
    list_display = ('owner', 'amount')


@admin.register(Transfer)
class TransferAdmin(ModelAdmin):
    list_display = ('origin_account', 'destination_account', 'amount', 'status')


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('recipient_email', 'created_at', 'text')
