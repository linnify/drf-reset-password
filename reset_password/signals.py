from django.dispatch import Signal

password_updated = Signal(providing_args=["user"])

custom_password_update = Signal(providing_args=["user", "password", "token"])
