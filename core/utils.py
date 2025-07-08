# core/utils.py
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

def send_transfer_email(to_email, subject, message):
    if to_email:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )

def send_sms(to_number, message_text):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_text,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)
