# tasks.py

from celery import shared_task
from django.core.mail import EmailMessage
from django.utils.timezone import now
from .models import User
from .utils import generate_pdf_statement

@shared_task
def send_monthly_statements():
    for user in User.objects.all():
        pdf = generate_pdf_statement(user)
        email = EmailMessage(
            'Monthly Account Statement',
            'Please find your monthly account statement attached.',
            'your_email@example.com',
            [user.email],
        )
        email.attach('statement.pdf', pdf.getvalue(), 'application/pdf')
        email.send()
