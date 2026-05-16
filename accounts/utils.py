import random

from django.core.mail import send_mail
from django.conf import settings

from .models import EmailOTP


def generate_otp():

    return str(random.randint(100000, 999999))


def send_otp_email(user):

    otp = generate_otp()

    EmailOTP.objects.update_or_create(
        user=user,
        defaults={
            'otp': otp
        }
    )

    subject = 'Your Login Verification Code'

    message = f'''
Hello {user.username},

Your verification code is:

{otp}

Do not share this code with anyone.
'''

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )