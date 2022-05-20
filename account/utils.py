from .models import Transaction
from django.contrib.auth.models import User






'''
Debit
'''

def perform_credit(request,credit_account,credit_amount,credit_type):
    ''' Perform Credit includes Load/Deposit Transactions'''

    if credit_account:
            current_balance = credit_account.balance
            Transaction.objects.create(account = credit_account,
            amount =credit_amount,
            type=credit_type,
            balance_after_transaction=current_balance + int(credit_amount),
            performed_by = request.user)

            credit_account.balance = credit_account.balance + int(credit_amount)
            updated_balance = credit_account.balance
            credit_account.save(update_fields=['balance'])
            print("Transaction Created Credited")  
            dir = { 'status':'True',
                'uid':credit_account.card_uid,
                'balance':updated_balance
                    }
            

            return dir,True
    else:
        dir = {

        }
        return dir,False



def perform_debit(request,debit_account,debit_amount,debit_type):
    ''' debit_account : account to be debited , debit_amount'''

    if debit_account.balance >= debit_amount:
        current_balance = debit_account.balance
        debit_transaction = Transaction.objects.create(account = debit_account,
        amount =debit_amount,
        type=debit_type,
        balance_after_transaction=current_balance - int(debit_amount),
        performed_by = request.user)

        debit_account.balance = debit_transaction.balance_after_transaction
        updated_balance = debit_account.balance
        debit_account.save(update_fields=['balance'])
        print("Transaction Created and Debited")  
        dir = { 'status':True,
            'uid':debit_account.card_uid,
            'balance':updated_balance
                }
        

        return dir,True
            
    else:
        dir = {
            'status':False,
            'uid':debit_account.card_uid,
            'balance':debit_account.balance

        }
        return dir,False




