from django.contrib.auth.models import User


class APISetUp:
    def setUpUrls(self):
        self.reset_password_create_url = "/reset-password"
        self.reset_password_submit_url = "/reset-password/submit"
        self.reset_password_validation_url = "/reset-password/token-validation"

    def check_password(self, username, password):
        user = User.objects.filter(username=username).first()

        return user.check_password(password)

    def reset_password_create(self, email):
        data = {
            'email': email
        }

        return self.client.post(
            self.reset_password_create_url,
            data,
            format='json',
        )

    def reset_password_submit(self, token, new_password):
        data = {
            'token': token,
            'password': new_password,
        }

        return self.client.post(
            self.reset_password_submit_url,
            data,
            format='json',
            QUERY_STRING="token=" + token,
        )

    def reset_password_validation(self, token):
        return self.client.get(
            self.reset_password_validation_url,
            format='json',
            QUERY_STRING="token="+token,
        )
