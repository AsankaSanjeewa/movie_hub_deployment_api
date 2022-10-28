from __future__ import absolute_import, unicode_literals
from smtplib import SMTPException
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from graphql_auth import constants
import requests
import json


@shared_task
def send_password_reset_mail(email, token):
    try:
        # Get dynamic link
        res = requests.post(
            'https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key'
            '=AIzaSyDT70Poe3crV2Dp7lc0hNFjvrhQ97IVtB4',
            headers={'content-type': 'application/json'},
            data=json.dumps({
                "dynamicLinkInfo": {
                    "domainUriPrefix": "https://mymovie.page.link",
                    "link": 'https://www.example.com/password-reset/' + token,
                    "androidInfo": {
                        "androidPackageName": "com.movie.hub.app"
                    }
                },
            })
        )
        res = res.json()
        send_mail(
            'Password Reset',
            strip_tags(render_to_string('email/password_reset_email.html', {'link': res['shortLink']})),
            'webmaster@localhost',
            [email],
            html_message=render_to_string('email/password_reset_email.html', {'link': res['shortLink']}),
            fail_silently=True,
        )
        return {'success': True, 'message': 'Password reset mail was successfully sent.'}
    except SMTPException:
        return constants.Messages.EMAIL_FAIL
