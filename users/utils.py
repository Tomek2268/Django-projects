from django.core.mail import send_mail
from django.conf import settings

from .models import Profile

def send_welcome_email(user):
    title = 'Welcome '+user.username+' !'
    message = 'I hope you will enjoy my website! Have fun!'
    send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

def create_profile(user):
    Profile.objects.create(
        user=user
    )