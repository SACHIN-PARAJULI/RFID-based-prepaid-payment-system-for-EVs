
from django.db import models
from django.contrib.auth.models  import User
from django.db.models.signals import pre_save


from datetime import date

from django.forms import ValidationError

from account.validators import validate_decimal, validate_hex 
TOLL_AMOUNT = 100

# Create your models here.
class Settings(models.Model):
    organization_name = models.CharField(max_length=200)
    organization_address = models.CharField(max_length=200)
    toll_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)


class Account(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    card_uid = models.CharField(max_length=10,unique=True,validators=[validate_decimal])
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    active = models.BooleanField(default=True)
    

    def __str__(self):
        return "{} - {}".format(self.name,self.card_uid)


TRANSACTION_CHOICES = [
    ('deposit','DEPOSIT'),
    ('toll-debit','TOLL DEBIT'),
    ('withdraw','WITHDRAW')]
class Transaction(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='transaction')
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    type = models.CharField(choices=TRANSACTION_CHOICES,max_length=20)
    balance_after_transaction = models.DecimalField(max_digits=12,decimal_places=2,blank=True)
    remarks = models.CharField(max_length=200,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="transactions_performed",null=True)

    def __str__(self):
        return "{} {}".format(self.account,self.type)
    
# def create_transaction(sender,instance,*args,**kwargs):
#     '''
#     perform transaction as per type
#     '''
#     if instance.type == 'deposit':
#         instance.account.balance += instance.amount
#         instance.account.save()
#         instance.balance_after_transaction = instance.account.balance

#     if instance.type == 'toll-debit':
#         if instance.account.balance >= TOLL_AMOUNT:
#             if instance.__class__.objects.filter(account=instance.account,type='toll-debit',timestamp__contains=date.today()).exists():
#                 print("Already Debited")
#                 raise ValidationError("Already Debited")
#             else:
#                 print("transaction not found")
#                 instance.account.balance -= TOLL_AMOUNT
#                 instance.account.save()
#                 instance.balance_after_transaction = instance.account.balance
#         else:
#             raise ValidationError("Low Balance")

# pre_save.connect(create_transaction,sender=Transaction)
