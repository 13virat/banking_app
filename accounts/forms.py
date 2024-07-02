from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import BankAccount, Transaction

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_number', 'balance']
        widgets = {
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TransactionForm(forms.ModelForm):
    transfer_to = forms.ModelChoiceField(queryset=BankAccount.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'transfer_to']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['transfer_to'].queryset = BankAccount.objects.filter(user=user)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
