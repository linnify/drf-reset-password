from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from reset_password.models import ResetPasswordToken


def to_link(field_name, column_name=None, field_show=None):
    def _to_link(obj):
        linked_object = getattr(obj, field_name)
        if linked_object is None:
            return "-"
        app_label = linked_object._meta.app_label
        model_name = linked_object._meta.model_name
        view_name = f"admin:{app_label}_{model_name}_change"
        link_url = reverse(view_name, args=[linked_object.pk])
        display_name = (
            getattr(linked_object, field_show) if field_show else linked_object
        )
        return format_html(f'<a href="{link_url}">{display_name}</a>')

    _to_link.short_description = column_name or field_name
    return _to_link


class ResetPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ("token", "expire_date", "status", to_link("user"))
    ordering = ("token",)
    list_per_page = 20


admin.site.register(ResetPasswordToken, ResetPasswordTokenAdmin)
