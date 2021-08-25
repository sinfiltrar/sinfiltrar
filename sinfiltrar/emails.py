from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User


def mail_staff(*args, **kwargs):
    """
    Wrapper for send email to staff users
    """
    kwargs['recipient_list'] = User.objects.filter(is_staff=True).values_list('email', flat=True)
    kwargs['subject'] = settings.EMAIL_SUBJECT_PREFIX +  kwargs['subject']
    kwargs['from_email'] = settings.DEFAULT_FROM_EMAIL

    send_mail(*args, **kwargs)
