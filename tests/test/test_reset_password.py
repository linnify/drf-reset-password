import json
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from reset_password.models import ResetPasswordToken, EmailProvider
from tests.test.api_set_up import APISetUp


class AuthTestCase(APITestCase, APISetUp):
    def setUp(self):
        self.setUpUrls()
        self.user1 = User.objects.create_user("user1", "user1@mail.com", "secret1")
        self.user2 = User.objects.create_user("user2", "user2@mail.com", "secret2")
        self.user3 = User.objects.create_user("user3@mail.com", "not-that-mail@mail.com", "secret3")
        self.user4 = User.objects.create_user("user4", "user4@mail.com")

    def test_try_reset_password_email_does_not_exist(self):
        response = self.reset_password_create("tas@mail.com")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        decoded_response = json.loads(response.content.decode())
        self.assertTrue("user" in decoded_response)

    def test_try_reset_password_email_does_not_exist_without_error(self):
        DRF_RESET_EMAIL = {
            'RETURN_EMAIL_NOT_FOUND_ERROR': False,
        }
        with self.settings(DRF_RESET_EMAIL=DRF_RESET_EMAIL):
            response = self.reset_password_create("tas@mail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_validate_token(self):
        self.assertEqual(ResetPasswordToken.objects.all().count(), 0)
        with patch.object(EmailProvider, 'send_email'):
            response = self.reset_password_create(email="user1@mail.com")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            self.assertEqual(ResetPasswordToken.objects.all().count(), 1)
            valid_token = str(ResetPasswordToken.objects.filter(user=self.user1).first().token)
            response = self.reset_password_validation(valid_token)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = self.reset_password_validation("bad token")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password(self):
        self.assertEqual(ResetPasswordToken.objects.all().count(), 0)
        with patch.object(EmailProvider, 'send_email'):
            response = self.reset_password_create(email=self.user2.email)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            self.assertEqual(ResetPasswordToken.objects.all().count(), 1)
            valid_token = str(ResetPasswordToken.objects.filter(user=self.user2).first().token)
            response = self.reset_password_submit(valid_token, "haha")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            user = User.objects.get(id=self.user2.id)
            self.assertEqual(user.check_password("haha"), True)

    def test_multiple_tokens(self):
        with patch.object(EmailProvider, 'send_email'):
            response = self.reset_password_create(email=self.user2.email)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(ResetPasswordToken.objects.all().count(), 1)

            response = self.reset_password_create(email=self.user2.email)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(ResetPasswordToken.objects.all().count(), 2)

            response = self.reset_password_create(email=self.user2.email)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(ResetPasswordToken.objects.all().count(), 3)
            self.assertEqual(ResetPasswordToken.objects.filter(status="invalid").count(), 2)

    def test_accepted(self):
        with patch.object(EmailProvider, 'send_email'):
            self.reset_password_create(email=self.user2.email)
            self.assertEqual(ResetPasswordToken.objects.all().count(), 1)
            valid_token = str(ResetPasswordToken.objects.filter(user=self.user2).first().token)
            response = self.reset_password_submit(valid_token, "haha")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = self.reset_password_create(email=self.user2.email)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(ResetPasswordToken.objects.all().count(), 2)

    def test_same_password(self):
        with patch.object(EmailProvider, 'send_email'):
            self.reset_password_create(email=self.user2.email)
            self.assertEqual(ResetPasswordToken.objects.all().count(), 1)
            valid_token = str(ResetPasswordToken.objects.filter(user=self.user2).first().token)

            response = self.reset_password_submit(valid_token, "secret2")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
