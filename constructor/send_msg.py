from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.shortcuts import render
from .models import Profile


def send(user, email, domain):

    subject = "Подтвреждение аккаунта."
    html_message = get_template('constructor/Message.html').render({
        'user': user,
        'domain': domain,
        'token': Profile.objects.get(user=User.objects.get(username=user)).token,
    })
    from_email='shievtsovm14@gmail.com'

    send_mail(subject, 'send', from_email, [email], fail_silently=True, html_message=html_message)
