from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from rest_framework import routers

from reset_password.views import ResetPasswordView

router = routers.DefaultRouter(trailing_slash=False)
router.register("reset-password", ResetPasswordView, basename="reset_password")

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r"^", include(router.urls)),
]
