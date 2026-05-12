from django.core.mail import send_mail
from django.conf import settings


def send_transaction_email(user, amount, transaction_type):

    subject = f'{transaction_type} Successful'

    message = f'''
Hello {user.first_name},

Your {transaction_type} request was successful.

Amount: {amount} BDT

Thank you for banking with us.
'''

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )