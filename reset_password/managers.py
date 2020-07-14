from django.db.models import Manager
from django.utils import timezone


class ResetPasswordManager(Manager):
    def get_valid_token(self, token: str):
        try:
            token = self.get(
                token=token,
                status=self.model.STATUS.PENDING.value,
                expire_date__gte=timezone.now(),
            )
        except self.model.DoesNotExist:
            return None

        return token

    def invalidate_existing_token(self, user):
        return self.filter(user=user, status="pending").update(status="invalid")
