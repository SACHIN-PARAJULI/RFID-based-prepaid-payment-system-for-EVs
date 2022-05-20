# @csrf_exempt
# def toll_debit(request):
#     if request.method == "POST":
#         data = request.POST

#         uid = data.get("uid")
#         try:
#             debit_account = Account.objects.get(card_uid = uid)
#         except Account.DoesNotExist:

#             '''return error stating account doesn't exist'''
#             debit_account = None
#             dir = {
#                 'status':False,
#                 'uid':uid,
#                 'message':"Account doesn't exists"
#             }
#             return JsonResponse(dir,status=404)
#         if debit_account:
#             current_balance = debit_account.balance
            
#             today = date.today()
#             transactions = Transaction.objects.filter(account = debit_account,type='toll-debit',timestamp__contains=today).count()
#             '''check if already transacted or not'''
#             if not transactions >= 1: 
        

#                 if(current_balance>=TOLL_AMOUNT):

#                     Transaction.objects.create(account = debit_account,amount =TOLL_AMOUNT,type='toll-debit',balance_after_transaction=current_balance-TOLL_AMOUNT,performed_by = User.objects.get(id=1))
#                     debit_account.balance = debit_account.balance - TOLL_AMOUNT
#                     updated_balance = debit_account.balance
#                     debit_account.save(update_fields=['balance'])
#                     print("Transaction Created and Debited")
#                     dir = {
#                         'status':True,
#                         'uid':debit_account.card_uid,
#                         'balance':updated_balance,
#                         'message':'Toll Debited'
#                             }
    
#                     return JsonResponse(dir)
#                 else:
#                     print('LOW BALANCE')
#                     dir = {
#                     'status':False,
#                     'uid':debit_account.card_uid,
#                     'balance':current_balance,
#                     'message':'Low Balance'
#                         }
#                     return JsonResponse(dir)
#             else:
#                 print("Toll Already Debited")
#                 dir = {
#                         'status':True,
#                     'uid':debit_account.card_uid,
#                     'balance':current_balance,
#                     'message':'Toll Already Debited'
#                 }
#                 return JsonResponse(dir)
        

            
#         else:
#             print("account doesn't exist")
#             # user does not exist
#             pass

#         if uid == 'CB62A221':
#             balance = 100000
#         elif uid == '674B7552':
#             balance = 500
#         else:
#             balance = 0
#         print(uid)
#         dir = {
#             'status':'ok',
#             'uid':uid,
#             'balance':balance
#         }
        
    
#         return JsonResponse(dir)
#     else:
#         dir = {
#             'status':False,
#             'message':'Only POST REQUEST'
#         }
#         return JsonResponse(dir,status=405)


# @csrf_exempt
# def deposit(request):
#     if request.method == "POST":
#         data = request.POST

#         uid = data.get("uid")
#         deposit_amount = data.get("amount")
#         try:
#             credit_account = Account.objects.get(card_uid = uid)
#         except Account.DoesNotExist:
#             credit_account = None
#         if credit_account:
#             current_balance = credit_account.balance
#             Transaction.objects.create(account = credit_account,
#             amount =deposit_amount,
#             type='deposit',
#             balance_after_transaction=current_balance + int(deposit_amount),
#             performed_by = User.objects.get(id=1))

#             credit_account.balance = credit_account.balance + int(deposit_amount)
#             updated_balance = credit_account.balance
#             credit_account.save(update_fields=['balance'])
#             print("Transaction Created and Deposited")  
#             dir = { 'status':'True',
#                 'uid':credit_account.card_uid,
#                 'balance':updated_balance
#                     }
            

#             return JsonResponse(dir)
#         else:
#             dir = {
#                 'status':'False'
#             }  
            
#             return JsonResponse(dir)  



# @csrf_exempt
# def deposit(request):


#     if request.method == "POST":
#         data = request.POST

#         uid = data.get("uid")
#         deposit_amount = data.get("amount")
#         try:
#             credit_account = Account.objects.get(card_uid = uid)
#         except Account.DoesNotExist:
#             credit_account = None
#         if credit_account:
#             current_balance = credit_account.balance
#             Transaction.objects.create(account = credit_account,
#             amount =deposit_amount,
#             type='deposit',
#             balance_after_transaction=current_balance + int(deposit_amount),
#             performed_by = User.objects.get(id=1))

#             credit_account.balance = credit_account.balance + int(deposit_amount)
#             updated_balance = credit_account.balance
#             credit_account.save(update_fields=['balance'])
#             print("Transaction Created and Deposited")  
#             dir = { 'status':'True',
#                 'uid':credit_account.card_uid,
#                 'balance':updated_balance
#                     }
            

#             return JsonResponse(dir)
#         else:
#             dir = {
#                 'status':'False'
#             }  
            
#             return JsonResponse(dir)  