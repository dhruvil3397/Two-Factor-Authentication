from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

# Token Generator:-------------
# We have to create token that will use in email confirmation url

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()
