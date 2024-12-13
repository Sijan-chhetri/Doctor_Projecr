# utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_appointment_confirmation_email(user_email, appointment_date, user_name):
    subject = 'Appointment Confirmed'
    message = f'Hello {user_name},\n\nYour appointment has been confirmed for {appointment_date}. Please come for your check-up.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


