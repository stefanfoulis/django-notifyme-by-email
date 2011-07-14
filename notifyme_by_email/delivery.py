#-*- coding: utf-8 -*-
from django.core.mail.message import EmailMultiAlternatives
from notifyme.delivery.base import BaseDeliveryBackend
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

class EmailBackend(BaseDeliveryBackend):
    identifier = 'email'

    def get_email(self, user):
        return user.email

    def get_from_email(self, user=None):
        return settings.DEFAULT_FROM_EMAIL

    def deliver_to(self, user, context, notice, language):
        to_email = self.get_email(user)
        context.update({
            'to_email': to_email,
        })
        subject = render_to_string(
            (
                "notifyme/notices/%s/email/subject.txt" % notice.identifier,
                "notifyme/notices/generic/email/subject.txt",
            ),
            context_instance=context
        )
        body = render_to_string(
            (
                "notifyme/notices/%s/email/body.txt" % notice.identifier,
                "notifyme/notices/generic/email/body.txt",
            ),
            context_instance=context
        )
        body_html = render_to_string(
            (
                "notifyme/notices/%s/email/body.html" % notice.identifier,
                "notifyme/notices/generic/email/body.html",
            ),
            context_instance=context
        )
        # TODO: send html
        send_mail(subject, body, self.get_from_email(user), [to_email])

        email_msg = EmailMultiAlternatives(subject, body, self.get_from_email(user),
            [to_email], headers={})
        email_msg.attach_alternative(body_html, "text/html")
        email_msg.send()
        
        