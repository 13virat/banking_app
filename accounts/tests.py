from django.test import TestCase
from django.contrib.auth.models import User
from .models import BankAccount, Transaction

class BankAccountTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.account = BankAccount.objects.create(user=self.user, account_number='1234567890', balance=1000.00)

    def test_account_creation(self):
        self.assertEqual(self.account.user.username, 'testuser')
        self.assertEqual(self.account.account_number, '1234567890')
        self.assertEqual(self.account.balance, 1000.00)

    def test_deposit_transaction(self):
        transaction = Transaction.objects.create(account=self.account, amount=500.00, transaction_type='deposit')
        transaction.execute_transaction()
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 1500.00)

    def test_withdrawal_transaction(self):
        transaction = Transaction.objects.create(account=self.account, amount=200.00, transaction_type='withdrawal')
        transaction.execute_transaction()
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 800.00)

    def test_transfer_transaction(self):
        recipient_account = BankAccount.objects.create(user=self.user, account_number='0987654321', balance=500.00)
        transaction = Transaction.objects.create(account=self.account, amount=300.00, transaction_type='transfer', transfer_to=recipient_account)
        transaction.execute_transaction()
        self.account.refresh_from_db()
        recipient_account.refresh_from_db()
        self.assertEqual(self.account.balance, 700.00)
        self.assertEqual(recipient_account.balance, 800.00)
