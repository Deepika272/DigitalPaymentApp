from django.shortcuts import render,redirect
from transactions.models import Creditcard,Transaction
from bankaccounts.models import Account,KYC
from django.urls import reverse_lazy



def credit_card_detail(request,number,account_number):
    account=Account.objects.get(account_number=account_number)
    credit_card=Creditcard.objects.get(number=number)

    context={
        'account':account,
        'credit_card':credit_card
    }
    return render(request,'account/credit_card_detail.html',context)

def credit_card_bill(request,card_id):
    card_detail=Creditcard.objects.get(card_id=card_id)
    account=Account.objects.get(user=request.user)
    if request.method=='POST':
        amount_entered=request.POST.get('amount')
        print(amount_entered)
        if account.account_balance<=0 or account.account_balance<int(amount_entered):
            print("insufficient amount")
        else:
            card_detail.amount+=int(amount_entered)
            account.account_balance-=int(amount_entered)
            print(card_detail.amount)
            account.save()
            card_detail.save()
            return redirect('transactions:credit_card',card_detail.number,card_detail.user.account.account_number)
       

    context={
        'card_detail':card_detail,
        'account':account
    }
    return render(request,'account/credit_card_bill.html',context)

def  credit_card_withdraw(request,card_id):
    card_detail=Creditcard.objects.get(card_id=card_id)
    account=Account.objects.get(user=request.user)
    if request.method=='POST':
        amount_entered=request.POST.get('amount')
        print(amount_entered)
        if int(amount_entered)<=0 or card_detail.amount<int(amount_entered):
            print("insufficient amount")
        else:
            card_detail.amount-=int(amount_entered)
            account.account_balance+=int(amount_entered)
            print(card_detail.amount)
            account.save()
            card_detail.save()
            return redirect('transactions:credit_card',card_detail.number,card_detail.user.account.account_number)
       

    context={
        'card_detail':card_detail,
        'account':account
    }
    return render(request,'account/withdraw_amount.html',context)

def card_delete(request,card_id):
    card_detail=Creditcard.objects.get(card_id=card_id)
    account=Account.objects.get(user=request.user)
    if card_detail.amount >0:
        account.account_balance+=card_detail.amount
        account.save()
        card_detail.delete()
    else:
       card_detail.delete()
    context={
        'card_detail':card_detail,
        'account':account
    }
    return render(request,'account/credit_card_detail.html',context) 

    