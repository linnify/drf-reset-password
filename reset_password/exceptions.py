class EmailProviderClassNotSet(Exception):
    message = "You need to set EMAIL_PROVIDER_CLASS in your settings"


class EmailProviderClassInvalid(Exception):
    message = (
        "Email provider is invalid please set the route "
        "correctly module.submodule.class"
    )


class RedirectLinkNotSet(Exception):
    message = (
        "You need to set up your redirect link for the default template"
    )


class AppNameNotSet(Exception):
    message = (
        "You need to set up your app name for the default template"
    )
