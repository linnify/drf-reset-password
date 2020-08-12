from django.apps import apps
from django.conf import settings
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from reset_password.models import ResetPasswordToken
from reset_password.serializers import (
    ResetPasswordSerializer,
    PasswordSerializer,
    TokenQueryParamsSerializer,
)


class ResetPasswordView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ResetPasswordToken.objects.all()
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        module, class_name = settings.AUTH_USER_MODEL.split(".")
        User = apps.get_model(module, class_name)
        user = User.objects.filter(email=request.data["email"]).first()
        if user:
            user = user.id
        serializer = self.get_serializer(data={"user": user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["GET"], detail=False, url_path="token-validation")
    def token_validation(self, request):
        token = self.validate_token(self.request.query_params)
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="submit")
    def change_password(self, request, *args, **kwargs):
        token = self.validate_token(self.request.query_params)

        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        PasswordSerializer(data=request.data).is_valid(raise_exception=True)
        token.update_password(request.data.get("password"))

        return Response(status=status.HTTP_200_OK)

    def validate_token(self, query_params):
        serializer = TokenQueryParamsSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        token = serializer.get_token()

        return ResetPasswordToken.objects.get_valid_token(token=token)
