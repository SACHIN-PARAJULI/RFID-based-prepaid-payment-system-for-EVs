from account.models import Transaction,Account
import django_filters
from django_filters import DateFilter,DateRangeFilter,DateTimeFilter,DateTimeFromToRangeFilter,CharFilter
from django import forms

class DateTimeInput(forms.DateTimeField):
    input_type = 'datetime'


class DateInput(forms.DateInput):
    input_type = 'date'

class TransactionFilter(django_filters.FilterSet):
    card_uid = CharFilter(field_name='account__card_uid',lookup_expr='exact',label="Card UID")
    date_range = DateRangeFilter(field_name='date',label='Predefined Date')
    account = CharFilter(field_name='account__name',lookup_expr='icontains',label="Account Name")
    start_date = DateFilter(field_name='date', lookup_expr='gte', label='FROM',widget=DateInput(attrs={'type': 'date'})) 
    end_date = DateFilter(field_name='date',label="TO",lookup_expr='lte',widget=DateInput(attrs={'type': 'date'}))
    
    
    # datetime_range = DateTimeFromToRangeFilter(field_name='timestamp',)
    class Meta:
        model = Transaction
        fields = ['type',]

class AccountFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',lookup_expr='icontains',label='Account Name')
    contact = CharFilter(field_name='contact',lookup_expr='exact',label='Contact')

    class Meta:
        model = Account
        fields = ['card_uid']