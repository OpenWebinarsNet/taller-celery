from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from accounts.exceptions import TransferError, AccountDoesntHaveEnoughMoney
from accounts.models import Account, Transfer, TransferStates
from accounts.tasks import transfer_money, notification


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

    notification.delay(account.owner, text='You have just done a withdraw')

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

    transfer_money.delay(origin_account_id, destination_account_id, amount, transfer.pk)

    notification.delay(email=origin_account.owner, text='You have just to do a transfer')
    notification.delay(email=destination_account.owner, text='You have just to receive a transfer')

    return HttpResponse(b'done', status=200)

