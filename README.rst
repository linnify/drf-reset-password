******************
DRF Reset Password
******************

This is an easy to include library that takes care of managing the reset password part of your application.
It offers 3 endpoints used for creating, validating and submitting the password change. The user if offered
the liberty to chose how the reset password link is sent to the user and where it will redirect the user.

Requirements
############

Python >= 3.7
Django >=3.0

We highly recommend and only officially support the latest patch release of each Python and Django series

Installation
############

The command to install the package from pypi using pip:

```
pip install drf-reset-password
```

Add ``reset-password`` to your ``INSTALLED_APPS`` in settings

::

    INSTALLED_APPS=[
        ...,
        'reset_password',
        ]

Configuration
#############

You can configure the library from the variable `DRF_RESET_EMAIL` that you will set in your settings.

::

    {
        'RESET_PASSWORD_EMAIL_TITLE': 'Reset Password',
        'RESET_PASSWORD_EMAIL_TEMPLATE': 'reset_email.html',
        'EMAIL_EXPIRATION_TIME': 24,
        'REDIRECT_LINK': 'dsa',
        'APP_NAME': 'test',
        'EMAIL_PROVIDER': 'reset_password.models.EmailProvider',
        'EMAIL_FIELD': 'email',
    }

``RESET_PASSWORD_EMAIL_TITLE`` - Sets the title of the email sent. ``RESET_PASSWORD_EMAIL_TITLE`` is on default on Reset Password.

``RESET_PASSWORD_EMAIL_TEMPLATE`` -  You can change the default template with your own template.``RESET_PASSWORD_EMAIL_TEMPLATE`` is on default on our default template.

``EMAIL_EXPIRATION_TIME`` - The amount of time it takes for the email to expire. ``EMAIL_EXPIRATION_TIME`` is on default on 24 hours.

``REDIRECT_LINK`` - The url of your redirect link inside the email (you can access it inside your own template with the variable ``link``).

``APP_NAME`` - The name of you app that will be mentioned inside the email.

``EMAIL_PROVIDER`` - The class which will be called to send the email (The class has to extend the class EmailProvider and implement the method send_email).

``EMAIL_FIELD`` - This is the field on the user that contains the email. If you are using django a user model
you should always have it on email. ``EMAIL_FIELD`` is on default on email.



Template Creation
#################

This is an example on how your template should look we give you 3 variables that you can access. Which are
``app_name``, ``link`` and ``email`` (this is the email of the user which had his password changed).


::

    <!DOCTYPE html>
    <html lang="en">
    <head>
    </head>
    <body>
      <p>Hello,</p>
      <p>Follow this link to reset your {{ app_name }} password for your {{ email }} account.</p>
      <p><a href='{{ link }}'>{{ link }}%</a></p>
      <p>If you didn’t ask to reset your password, you can contact us.</p>
      <p>Thanks,</p>
      <p>Your {{ app_name }} team</p>
    </body>
    </html>

Final steps for set up
######################

When you are done with configuring your reset_password app you can add it to your urls and start making calls.

::

    from django.conf.urls import url
    from django.urls import include
    from rest_framework import routers
    from reset_password.views import ResetPasswordView

    router = routers.DefaultRouter(trailing_slash=False)
    router.register("reset-password", ResetPasswordView, basename="reset_password")
    urlpatterns = [
        ...,
        url(r"^", include(router.urls)),
    ]

Endpoints
#########

The app has 3 endpoints: one for generating the email for reset password, one for validating the token inside 
the email and one for changing the password.

Create Endpoint
###############

This endpoint receives the email address and creates and calls for the ``EMAIL_PROVIDER`` to send the email to the
user.

::

    reset-password/ -> POST


::

    {
      "email": "example@google.com"
    }

It has an empty response with 201 if successful and 400 if email is not valid.

Token Validation
################

This endpoint receives the token through the query param ``token`` and it verifies if it is valid.

::

    reset-password/token-validation -> POST


::

    {

    }

It has an empty response with 200 if successful and 400 if token is not valid.


Change Password
###############

This endpoint receives the token through the query param ``token`` and it verifies if it is valid. and then changes
the user's password with the one sent in the body

::

    reset-password/submit -> POST

::

    {
      "password": "password"
    }

It has an empty response with 200 if successful and 400 if token is not valid or the password sent.



Good luck using it and if you have any question or suggestions please contact us



