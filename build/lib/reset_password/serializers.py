from rest_framework import serializers

from reset_password.models import ResetPasswordToken


class ResetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResetPasswordToken
        fields = ("user",)

    def create(self, validated_data):
        return super().create(validated_data)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, required=True)

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        raise NotImplementedError()


class TokenQueryParamsSerializer(serializers.Serializer):
    token = serializers.UUIDField(format="hex_verbose")

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        raise NotImplementedError()

    def get_token(self):
        return self.initial_data.get("token")
