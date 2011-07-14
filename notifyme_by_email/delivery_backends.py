#-*- coding: utf-8 -*-
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from notifyme.delivery_backends.base import BaseDeliveryBackend


class EmailBackend(BaseDeliveryBackend):
    identifier = 'email'

    def get_email(self, user):
        return user.email

    def get_from_email(self, user=None):
        return settings.DEFAULT_FROM_EMAIL

    def deliver_to(self, user, context, notification, language):
        to_email = self.get_email(user)
        context.update({
            'to_email': to_email,
        })
        subject = render_to_string(
            (
                "notifyme/notification_types/%s/email/subject.txt" % notification.identifier,
                "notifyme/notification_types/generic/email/subject.txt",
            ),
            context_instance=context
        )
        body = render_to_string(
            (
                "notifyme/notification_types/%s/email/body.txt" % notification.identifier,
                "notifyme/notification_types/generic/email/body.txt",
            ),
            context_instance=context
        )
        body_html = render_to_string(
            (
                "notifyme/notification_types/%s/email/body.html" % notification.identifier,
                "notifyme/notification_types/generic/email/body.html",
            ),
            context_instance=context
        )
        # send the HTML Email
        email_msg = EmailMultiAlternatives(subject, body, self.get_from_email(user),
            [to_email], headers={})
        email_msg.attach_alternative(body_html, "text/html")
        email_msg.send()
        
        