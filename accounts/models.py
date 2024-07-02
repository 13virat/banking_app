from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone



class Account(models.Model):
    ACCOUNT_TYPES = [
        ('SAVINGS', 'Savings'),
        ('CHECKING', 'Checking'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.account_type}'

    
class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.user.username} - {self.account_number}'

class Transaction(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    timestamp = models.DateTimeField(default=timezone.now)
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer')
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transfer_to = models.ForeignKey(BankAccount, null=True, blank=True, on_delete=models.CASCADE, related_name='transfers')

    def __str__(self):
        return f'{self.transaction_type.capitalize()} - {self.amount}'

    def execute_transaction(self):
        if self.transaction_type == 'deposit':
            self.account.balance += self.amount
        elif self.transaction_type == 'withdrawal':
            if self.amount > self.account.balance:
                raise ValueError("Insufficient balance.")
            self.account.balance -= self.amount
        elif self.transaction_type == 'transfer':
            if self.amount > self.account.balance:
                raise ValueError("Insufficient balance for transfer.")
            if not self.transfer_to:
                raise ValueError("Transfer to account must be specified.")
            self.account.balance -= self.amount
            self.transfer_to.balance += self.amount
            self.transfer_to.save()
        self.account.save()
        self.save()