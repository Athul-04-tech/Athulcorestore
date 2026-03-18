import random

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    from django.core.mail import send_mail
    from django.conf import settings
    
    subject = "Email Verification OTP"
    message = f"Your verification OTP is {otp}. It is valid for 5 minutes."

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )

