from django import forms
from .models import Settings, Transaction,Account



class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('account','type','amount','remarks')
    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.fields['account'].disabled= True
        self.fields['type'].disabled = True



class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('account','type','amount','remarks')
    def __init__(self, *args, **kwargs):
        super(WithdrawForm, self).__init__(*args, **kwargs)
        self.fields['account'].disabled= True
        self.fields['type'].disabled = True



class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['balance'].disabled= True


        

class UpdateTollForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(UpdateTollForm, self).__init__(*args, **kwargs)
        self.fields['organization_name'].disabled= True
        self.fields['organization_address'].disabled = True

class UpdateOrganizationForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('organization_name','organization_address')
    # def __init__(self, *args, **kwargs):
    #     super(UpdateTollForm, self).__init__(*args, **kwargs)
    #     self.fields['toll_amount'].disabled= True
    #     self.fields['organization_address'].disabled = True

class SearchForm(forms.Form):
    card_uid = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),label='Scan Card UID', max_length=10)

    