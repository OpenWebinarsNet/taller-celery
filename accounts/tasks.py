import random
import time

from django.db import transaction

from accounts.exceptions import TransferError
from accounts.models import Notification, Account, Transfer, TransferStates
from bank.celery_app import app


@app.task
def notification(email: str, text: str):
    time.sleep(5)
    Notification.objects.create(recipient_email=email, text=text)


@app.task(autoretry_for=(TransferError,), retry_backoff=True, max_retries=10)
@transaction.atomic
def transfer_money(origin_account_id: int, destination_account_id: int, amount: float, transfer_id: int):
    error = random.randint(1, 3) == 3
    if error:
        raise TransferError()

    time.sleep(5)

    origin_account = Account.objects.get(pk=origin_account_id)
    destination_account = Account.objects.get(pk=destination_account_id)

    origin_account.amount -= amount
    destination_account.amount += amount

    origin_account.save()
    destination_account.save()

    transfer = Transfer.objects.get(pk=transfer_id)
    transfer.status = TransferStates.FINISHED
    transfer.save()
