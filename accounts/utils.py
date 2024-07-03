# utils.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from .models import Transaction

def generate_pdf_statement(user):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(100, 750, f"Account Statement for {user.username}")

    # Fetch the user's transactions
    transactions = Transaction.objects.filter(account__user=user).order_by('-timestamp')

    # Set initial coordinates for drawing text
    y = 720
    for transaction in transactions:
        if y < 100:  # Create a new page if the current page is full
            c.showPage()
            y = 750

        # Draw transaction details
        c.drawString(100, y, f"Date: {transaction.timestamp}, Type: {transaction.transaction_type}, Amount: {transaction.amount}")
        y -= 20  # Move down the page for the next transaction

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
