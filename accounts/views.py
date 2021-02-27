import random
import time

from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from accounts.exceptions import TransferError, AccountDoesntHaveEnoughMoney
from accounts.models import Notification, Account, Transfer, TransferStates


@require_POST
@csrf_exempt
def withdraw_view(request: WSGIRequest):
    account_id: int = int(request.POST['account'])
    amount: float = float(request.POST['amount'])

    account = Account.objects.get(id=account_id)

    if amount > account.amount:
        raise AccountDoesntHaveEnoughMoney()

    account.amount -= amount
    account.save()

    notification(account.owner, text='You have just done a withdraw')

    return HttpResponse(b'done', status=200)


@require_POST
@csrf_exempt
def transfer_view(request: WSGIRequest):
    origin_account_id: int = int(request.POST['origin_account'])
    destination_account_id: int = int(request.POST['destination_account'])
    amount: float = float(request.POST['amount'])

    origin_account = Account.objects.get(id=origin_account_id)
    destination_account = Account.objects.get(id=destination_account_id)

    if amount > origin_account.amount:
        return AccountDoesntHaveEnoughMoney()

    transfer = Transfer.objects.create(origin_account_id=origin_account_id,
                                       destination_account_id=destination_account_id, amount=amount)
    try:
        transfer_money(origin_account_id, destination_account_id, amount)
    except TransferError:
        transfer.status = TransferStates.ERROR
        transfer.save()
        return HttpResponse(b'error', status=500)

    transfer.status = TransferStates.FINISHED
    transfer.save()

    notification(email=origin_account.owner, text='You have just to do a transfer')
    notification(email=destination_account.owner, text='You have just to receive a transfer')

    return HttpResponse(b'done', status=200)


def notification(email: str, text: str):
    time.sleep(5)
    Notification.objects.create(recipient_email=email, text=text)


@transaction.atomic
def transfer_money(origin_account_id: int, destination_account_id: int, amount: float):
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
