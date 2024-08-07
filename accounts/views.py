from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from .models import BankAccount, Transaction
from .forms import BankAccountForm, TransactionForm
from .forms import SignUpForm
import logging
# views.py


from django.http import FileResponse

from .utils import generate_pdf_statement

@login_required
def download_statement(request):
    pdf = generate_pdf_statement(request.user)
    return FileResponse(pdf, as_attachment=True, filename='statement.pdf')

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})




@login_required
def create_account(request):
    try:
        if request.method == 'POST':
            form = BankAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('account_list')
        else:
            form = BankAccountForm()
    except Exception as e:
        logger.error(f"Error creating account: {e}")
        form = BankAccountForm()
    return render(request, 'accounts/create_account.html', {'form': form})

@login_required
def account_list(request):
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(BankAccount, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            try:
                if transaction.transaction_type == 'transfer' and transaction.transfer_to:
                    transfer_to_account = form.cleaned_data['transfer_to']
                    if transaction.amount > account.balance:
                        raise ValueError("Insufficient balance for transfer.")
                    account.balance -= transaction.amount
                    transfer_to_account.balance += transaction.amount
                    account.save()
                    transfer_to_account.save()
                else:
                    transaction.execute_transaction()
            except ValueError as e:
                logger.warning(f"Transaction error: {e}")
                return render(request, 'accounts/account_detail.html', {'account': account, 'transactions': transactions, 'form': form, 'error': str(e)})
            transaction.save()
            return redirect('account_detail', account_id=account_id)
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'accounts/account_detail.html', {'account': account, 'transactions': transactions, 'form': form})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')
    return render(request, 'accounts/transaction_history.html', {'transactions': transactions})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def create_transaction(request, account_id):
    account = get_object_or_404(BankAccount, id=account_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            try:
                transaction.execute_transaction()
            except ValueError as e:
                return render(request, 'accounts/transaction_error.html', {'error': str(e)})
            return redirect('account_detail', account_id=account_id)
    else:
        form = TransactionForm()
    return render(request, 'accounts/create_transaction.html', {'form': form})

