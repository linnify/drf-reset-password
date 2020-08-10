import uuid
from datetime import timedelta
from enum import Enum
from pydoc import locate

import django
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

from reset_password.exceptions import (
    EmailProviderClassNotSet,
    EmailProviderClassInvalid,
    RedirectLinkNotSet, AppNameNotSet)
from reset_password.managers import ResetPasswordManager
from django.conf import settings


class StatusType(Enum):
    ACCEPTED = "accepted"
    PENDING = "pending"
    INVALID = "invalid"


STATUS_TYPES = [(e.value, e.value) for e in StatusType]


class ResetPasswordToken(models.Model):
    STATUS = StatusType
    token = models.UUIDField(primary_key=False, default=uuid.uuid4)
    expire_date = models.DateTimeField(null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reset_password",
        on_delete=models.CASCADE,
    )
    status = models.CharField(choices=STATUS_TYPES, default=StatusType.PENDING.value, max_length=100)
    created = models.DateTimeField(default=django.utils.timezone.now)
    objects = ResetPasswordManager()

    def save(self, *args, **kwargs):

        if not self.id:
            ResetPasswordToken.objects.invalidate_existing_token(user=self.user)
            self.expire_date = timezone.now() + timedelta(minutes=self._get_email_expiration_time(),)
            self.send_email()

        return super(ResetPasswordToken, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.expire_date}-{self.token}-{self.status}"

    def send_email(self):
        mail = self._get_email_provider()
        email = self._get_user_email()

        content = render_to_string(
            self._get_email_template(),
            {"link": self._get_redirect_link()+str(self.token), "app_name": self._get_app_name(), "email": email},
        )
        return mail.send_email(email, self._get_email_title(), content)

    def update_password(self, password: str):
        self.user.set_password(password)
        self.user.save()
        self.status = StatusType.ACCEPTED.value
        self.save()

    def _get_user_email(self):
        if settings.DRF_RESET_EMAIL.get("EMAIL_FIELD"):
            return self.user.__getattribute__(settings.DRF_RESET_EMAIL["EMAIL_FIELD"])
        else:
            return self.user.email

    def _get_email_provider(self):
        if not settings.DRF_RESET_EMAIL.get("EMAIL_PROVIDER"):
            raise EmailProviderClassNotSet()

        email_class = locate(settings.DRF_RESET_EMAIL["EMAIL_PROVIDER"])
        if not email_class:
            raise EmailProviderClassInvalid()
        return email_class()

    def _get_email_template(self):
        return settings.DRF_RESET_EMAIL["RESET_PASSWORD_EMAIL_TEMPLATE"] if settings.DRF_RESET_EMAIL.get("RESET_PASSWORD_EMAIL_TEMPLATE") else "reset_password_email.html"

    def _get_email_title(self):
        return settings.DRF_RESET_EMAIL["RESET_PASSWORD_EMAIL_TITLE"] if settings.DRF_RESET_EMAIL.get("RESET_PASSWORD_EMAIL_TITLE") else "Reset Password"

    def _get_email_expiration_time(self):
        return settings.DRF_RESET_EMAIL["EMAIL_EXPIRATION_TIME"] if settings.DRF_RESET_EMAIL.get("EMAIL_EXPIRATION_TIME") else 24

    def _get_redirect_link(self):
        if not settings.DRF_RESET_EMAIL.get("REDIRECT_LINK"):
            raise RedirectLinkNotSet()
        return settings.DRF_RESET_EMAIL.get("REDIRECT_LINK")

    def _get_app_name(self):
        if not settings.DRF_RESET_EMAIL.get("APP_NAME"):
            raise AppNameNotSet()
        return settings.DRF_RESET_EMAIL.get("APP_NAME")


class EmailProvider:
    def send_email(self, email, title, content):
        if settings.DRF_RESET_EMAIL.get("TEST_ENV"):
            return
        else:
            raise NotImplementedError("You need to implement this method on your email provider")
