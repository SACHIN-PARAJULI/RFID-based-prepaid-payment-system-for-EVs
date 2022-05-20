from datetime import datetime
from MySQLdb import Timestamp
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from account.forms import AccountForm, DepositForm,WithdrawForm, SearchForm, UpdateTollForm,UpdateOrganizationForm,AccountUpdateForm
from account.validators import is_hex, is_valid_decimal
from .models import Account, Settings,Transaction
from django.core.paginator import Paginator
from .filters import AccountFilter, TransactionFilter
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login,logout
from django.contrib import messages
import requests as rq
from django.db.models import Sum


'''Imports for api'''
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from django.contrib.auth.decorators import login_required
'''Get Toll amount from settings'''
# settings_object,created = Settings.objects.get_or_create(id=1,defaults={'organization_name':'SMART CARD NEPAL','organization_address':'Dharan,Sunsari','toll_amount':100})
# TOLL_AMOUNT = settings_object.toll_amount



#  for report generation

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

from .utils import perform_credit,perform_debit








def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('account:index')
        else:
            messages.info(request,"Username or Password Incorrect")
 
    context ={}
    return render(request,'dashboard/login.html',context)

@login_required(login_url='account:admin-login')
def logoutPage(request):
    logout(request)
    messages.info(request,"Logout Successfully")
    return redirect('account:admin-login')




@login_required(login_url='account:admin-login')
def index(request):
    print("TODAY DATE".format(str(date.today())))
    print(date.today())
    '''todays data'''
    total_debit_transaction_today = Transaction.objects.filter(type='toll-debit',date = date.today()).aggregate(Sum('amount'))['amount__sum']
    total_deposit_transaction_today = Transaction.objects.filter(type='deposit',date = date.today()).aggregate(Sum('amount'))['amount__sum']
    total_users = Account.objects.all().count()
    print(total_debit_transaction_today)
    context = {
        'index_page':True,
        'total_debit_today':total_debit_transaction_today,
        'total_deposit_today':total_deposit_transaction_today,
        'total_users':total_users,


    }
    return render(request,'dashboard/home.html',context)




class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        print(request.user)
        content = {'message': 'Hello, World!'}
        return Response(content)





class DebitRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
    
        uid = request.POST.get('uid')
        '''decimal from hex'''

        dec_uid = int(uid,16)
        print(dec_uid)
        try:
            # debit_account = Account.objects.get(card_uid = uid)
            debit_account = Account.objects.get(card_uid = dec_uid)
        except Account.DoesNotExist:

            '''return error stating account doesn't exist'''
            debit_account = None
            dir = {
                'status':False,
                'uid':uid,
                'message':"Account doesn't exists"
            }
            return Response(dir,status=404)
        if debit_account:
            current_balance = debit_account.balance
            
            today = date.today()
            transactions = Transaction.objects.filter(account = debit_account,type='toll-debit',date=today).count()
            '''check if already transacted or not'''
            if not transactions >= 1: 
                
                settings_object,created = Settings.objects.get_or_create(id=1,
                defaults={
                    'organization_name':'SMART CARD NEPAL',
                'organization_address':'Dharan,Sunsari',
                'toll_amount':100})
                toll_amount = settings_object.toll_amount

                if(current_balance>=toll_amount):
                    ''' if current balance is greater than toll amount  create debit transaction '''
                    Transaction.objects.create(account = debit_account,amount =toll_amount,
                    type='toll-debit',
                    balance_after_transaction=current_balance-toll_amount,
                    performed_by = request.user,
                    remarks = 'TOLL DEBIT by #{}'.format(request.user))

                    debit_account.balance = debit_account.balance - toll_amount
                    updated_balance = debit_account.balance
                    debit_account.save(update_fields=['balance'])
                    print("Transaction Created and Debited")
                    dir = {
                        'status':True,
                        'uid':debit_account.card_uid,
                        'balance':updated_balance,
                        'message':'Toll Debited'
                            }
    
                    return Response(dir)
                else:
                    print('LOW BALANCE')
                    dir = {
                    'status':False,
                    'uid':debit_account.card_uid,
                    'balance':current_balance,
                    'message':'Low Balance'
                        }
                    return Response(dir)
            else:
                print("Toll Already Debited")
                dir = {
                        'status':True,
                    'uid':debit_account.card_uid,
                    'balance':current_balance,
                    'message':'Toll Already Debited'
                }
                return Response(dir)
        




@login_required(login_url='account:admin-login')
def transaction_report(request):
    data = request.GET

    id = data.get("id")
    transaction_account = Account.objects.get(id = int(id))
    transactions = Transaction.objects.filter(account = transaction_account)

    context = {
        'transaction_account':transaction_account,
        'transactions':transactions,
    }

    return render(request,'account/transaction_history.html',context)


@login_required(login_url='account:admin-login')
def load_balance(request,id):
    
    credit_account = Account.objects.get(id=id)
    transaction_instance = Transaction(account = credit_account,type='deposit')

    form = DepositForm(instance=transaction_instance)
    if request.method == 'POST':
        form = DepositForm(request.POST,instance = transaction_instance)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            response , success = perform_credit(request,credit_account,amount,credit_type='deposit')
            if success:
                messages.success(request,'Balance Loaded \n New Balance is :Rs {}'.format(str(response['balance'])))
                return redirect('account:index')
    
    context = {
        'form':form,
    }

    return render(request,'account/deposit.html',context)


@login_required(login_url='account:admin-login')
def withdraw_balance(request,id):
    
    withdraw_account = Account.objects.get(id=id)
    transaction_instance = Transaction(account = withdraw_account,type='withdraw')

    form = WithdrawForm(instance=transaction_instance)
    if request.method == 'POST':
        form = WithdrawForm(request.POST,instance = transaction_instance)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            response , success = perform_debit(request,withdraw_account,amount,debit_type='withdraw')
            if success:
                messages.success(request,'Withdraw Success For {}\n New Balance is {}'.format(withdraw_account,str(response['balance'])))
                return redirect('account:index')
            else:
                messages.success(request,"ERROR OCCURED \n Current Balance is Rs {}".format(str(response['balance'])))
    
    context = {
        'form':form,
    }

    return render(request,'account/withdraw.html',context)

@login_required(login_url='account:admin-login')
def add_new_account(request):
    account_form = AccountForm()

    card_uid = request.GET.get('card_uid')
    print(card_uid)
    if not card_uid == '':
        new_account = Account(card_uid = card_uid)
        account_form = AccountForm(instance=new_account)
    
    if request.method  == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            initial_credit_balance = account_form.cleaned_data['balance']
            new_account = account_form.save(commit=False)
            new_account.balance = 0
            new_account.save()
            response , success = perform_credit(request,new_account, initial_credit_balance,credit_type='deposit')
            if success:
                messages.success(request,'Account Created ')
                return redirect('account:index')


    context = {
        'form':account_form
    }

    return render(request,'account/new_account.html',context)

@login_required(login_url='account:admin-login')
def update_account(request,id):
    account = Account.objects.get(id=id)
    account_form = AccountUpdateForm(instance=account)
        
    
    if request.method  == 'POST':
        account_form = AccountUpdateForm(request.POST,instance=account)
        if account_form.is_valid():
            updated_account = account_form.save()
            # initial_balance = account_form.cleaned_data['balance']
            # new_account = account_form.save(commit=False)
            # new_account.balance = 0
            # new_account.save()
            # response , success = perform_load(request,new_account, initial_balance)
            messages.success(request,'Account Updated ')
            return redirect('account:transaction-history',id=updated_account.id)


    context = {
        'form':account_form
    }

    return render(request,'account/update_account.html',context)


def add_account_card(request):

    pass


@login_required(login_url='account:admin-login')
def search_account(request):
    data = request.GET
    myquery = data.get('query')
    context = {}

    if not myquery == '':
        ''' check if query is digit and its length is 10'''
        if myquery.isdigit() and len(myquery) == 10:
            if is_valid_decimal(myquery):
                print('decimal query')
                ''' decimal uid'''
                context['results'] = Account.objects.filter(card_uid = myquery)
                if not context['results']:
                    context['card_search'] = {'flag':True, 'card_uid':myquery}
                # context['type'] = {
                #     query = 
                # }
            else:
                print('phone number')
                ''' 10 digits contact number '''
                context['results']=Account.objects.filter(contact=myquery)  
        
        else:
            print('string')
            '''query is normal string'''
            context['results'] = Account.objects.filter(name__icontains=myquery)

    
    return render(request,'account/search_account.html',context)





@login_required(login_url='account:admin-login')
def transaction_history(request,id):
    transaction_account = Account.objects.get(id = int(id))
    transactions = Transaction.objects.filter(account = transaction_account).order_by('-timestamp')

    context = {
        'transaction_account':transaction_account,
        'transactions':transactions,
    }

    return render(request,'account/transaction_history.html',context)

@login_required(login_url='account:admin-login')
def update_toll(request):
    settings_object,created = Settings.objects.get_or_create(id=1,defaults={'organization_name':'SMART CARD NEPAL','organization_address':'Dharan,Sunsari','toll_amount':100})

    settings_form = UpdateTollForm(instance= settings_object)

    if request.method == 'POST':
        settings_form = UpdateTollForm(request.POST,instance=settings_object)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request,'Toll Updated Successfully')
            return redirect('account:index')
    
    context = {
        'settings_page':True,
        'form_title':'Update Toll',
        'form_button':'Update',
        'form':settings_form
    }

    return render(request,'dashboard/settings.html',context)

@login_required(login_url='account:admin-login')
def update_organization(request):
    settings_object,created = Settings.objects.get_or_create(id=1,defaults={'organization_name':'SMART CARD NEPAL','organization_address':'Dharan,Sunsari','toll_amount':100})

    settings_form = UpdateOrganizationForm(instance= settings_object)

    if request.method == 'POST':
        settings_form = UpdateOrganizationForm(request.POST,instance=settings_object)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request,'Organization Details Updated Successfully')
            return redirect('account:index')
    
    context = {
        'settings_page':True,
        'form_title':'Update Organization Detail',
        'form_button':'Update',
        'form':settings_form
    }

    return render(request,'dashboard/settings.html',context)


@login_required(login_url='account:admin-login') 
def transaction_history(request,id):
    transaction_account = Account.objects.get(id = int(id))
    # transactions = Transaction.objects.filter(account = transaction_account).order_by('-timestamp')


    context = {
        'transaction_account':transaction_account,
        # 'transactions':transactions,
    }

    return render(request,'account/transaction_history.html',context)

@login_required(login_url='account:admin-login') 
def transactionfilter(request):

    context = {}
    context['transaction_page'] = True
    p = TransactionFilter(request.GET, queryset=Transaction.objects.select_related('account','performed_by').order_by('-timestamp'))
    # p = TransactionFilter(request.GET, queryset=Transaction.objects.all().order_by('-timestamp'))
    

    toll_total = p.qs.filter(type='toll-debit').aggregate(Sum('amount'))['amount__sum']
    withdraw_total = p.qs.filter(type='withdraw').aggregate(Sum('amount'))['amount__sum']
    deposit_total = p.qs.filter(type='deposit').aggregate(Sum('amount'))['amount__sum']
    # total_credit  = p.qs.filter(type='deposit').aggregate(Sum('amount'))['amount__sum']
    print('Toll Total: {}'.format(str(toll_total)))
    print('Withdraw Total: {}'.format(str(withdraw_total)))
    print('Deposit Total: {}'.format(str(deposit_total)))
    paginated_filter = Paginator(p.qs,per_page=10)
    page_number = request.GET.get('page')
    transactions = paginated_filter.get_page(page_number)
    context['p'] = p
    context['transactions'] = transactions
    context['toll_total'] = toll_total
    context['withdraw_total'] = withdraw_total
    context['deposit_total'] = deposit_total

    return render(request,'account/transaction_filter.html',context)





@login_required(login_url='account:admin-login') 
def transactionpartial(request):

    context = {}
    # p = TransactionFilter(request.GET, queryset=Transaction.objects.all().order_by('-timestamp'))
    p = TransactionFilter(request.GET, queryset=Transaction.objects.select_related('account','performed_by').order_by('-timestamp'))




    paginated_filter = Paginator(p.qs,per_page=10)
    page_number = request.GET.get('page')
    transactions = paginated_filter.get_page(page_number)
    context['p'] = p
    context['transactions'] = transactions

    return render(request,'account/partials/transaction_filter_partial.html',context)



@login_required(login_url='account:admin-login') 
def accountfilter(request):

    context = {}
    p = AccountFilter(request.GET, queryset=Account.objects.all())



    paginated_filter = Paginator(p.qs,per_page=10)
    page_number = request.GET.get('page')
    accounts = paginated_filter.get_page(page_number)
    context['account_page'] = True
    context['p'] = p
    context['accounts'] = accounts

    return render(request,'account/account_filter.html',context)



@login_required(login_url='account:admin-login') 
def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html= template.render(context_dict)
    print(html)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None



class GenerateTransactionInvoice(View):
    def get(self,request,id,*args,**kwargs):
        mytransaction = Transaction.objects.get(id=id)
        settings = Settings.objects.get(id=1)

        data = {}
        data['settings'] = settings
        data['account_name']=mytransaction.account.name
        data['account_contact'] = mytransaction.account.contact
        data['amount'] = str(mytransaction.amount)
        data['transaction_type'] = mytransaction.type.upper()
        data['transaction_date'] = mytransaction.date

        if mytransaction.type == 'deposit':
            template_path = 'account/transaction/deposit_report.html'
        elif mytransaction.type == 'withdraw':
            template_path = 'account/transaction/withdraw_report.html'
        else:
            template_path = 'account/transaction/toll_report.html'
        context = {'myvar': 'this is your template context'}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(data)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response,)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response





        # pdf = render_to_pdf('account/transaction/report.html',data)

        # return HttpResponse(pdf,content_type='application/json')

        # force download
        # if pdf:
        #     response = HttpResponse(pdf,content_type='application/json')
        #     filename = "%s TRANSACTION.pdf"%(data['transaction_type'])
        #     content = "inline; filename='%s'"%(filename)
        #     response['Content-Disposition'] = content
        #     return response
        # return HttpResponse('Not Found')


@login_required(login_url='account:admin-login') 
def render_pdf_view(request):
    template_path = 'account/transaction/report.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



@login_required(login_url='account:admin-login')
def get_token(request):

    token,created = Token.objects.get_or_create(user=request.user)

    my_token = str(token)
    context = {
        'token': my_token
    }

    return render(request,'myadmin/token.html',context)

def help_deposit(request):
    search_form = SearchForm()
    card_uid = request.GET.get('card_uid')
    context = {
        'deposit_page':True,
        'search_form':search_form,
    }
    if not card_uid == '' and not card_uid  is None:
        account = Account.objects.filter(card_uid = card_uid)
        if account.count() ==1:
            account = account.first()
            messages.success(request,'Account : {} Current Balance is Rs {}'.format(account,str(account.balance)))
            return redirect('account:load-balance',id=account.id)
        else:
            messages.success(request,'Account Not Found for - {}'.format(card_uid))

    

    return render(request,'account/help_deposit.html',context)