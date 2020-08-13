from django.dispatch import Signal

password_updated = Signal(providing_args=["user"])
