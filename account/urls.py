from account import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'account'
urlpatterns =[
    path('',views.index,name='index'),
    path('admin-login',views.loginPage,name='admin-login'),
    path('admin-logout',views.logoutPage,name='admin-logout'),
    path('get-my-token',views.get_token,name='get-token'),


    path('account/search',views.search_account,name='search-account'),
    path('account/add-new-account',views.add_new_account,name='add-new-account'),
    path('account/update-account/<int:id>',views.update_account,name='update-account'),
    path('account/load-balance/<int:id>',views.load_balance,name="load-balance"),
    path('account/withdraw-balance/<int:id>',views.withdraw_balance,name="withdraw-balance"),


    path('account/help-deposit',views.help_deposit,name='help-deposit'),
    path('test',views.render_pdf_view,name='render_pdf'),

    path('account/transaction-filter',views.transactionfilter,name='transaction-filter'),
    path('account/account-filter',views.accountfilter,name='account-filter'),
    path('account/transaction/download-pdf/<int:id>',login_required(views.GenerateTransactionInvoice.as_view()),name='transaction-pdf'),
    path('account/transaction-partial',views.transactionpartial,name='transaction-partial'),
    path('account/transaction-history/<int:id>',views.transaction_history,name='transaction-history'),
    path('settings/update-toll',views.update_toll,name='update-toll'),
    path('settings/update-organization',views.update_organization,name='update-organization'),



    path('api/test',views.HelloView.as_view(),name='test'),

    path('api/get-auth-token', obtain_auth_token,name='obtain-auth-token'),
    path('api/toll-debit',views.DebitRequestView.as_view(),name='toll-debit'),


    # path('api/deposit',views.deposit,name="deposit"),
    # path('api/toll-debit',views.toll_debit,name="toll-debit"),
    # path('api/transaction-report',views.transaction_report,name='transaction-report'),



]