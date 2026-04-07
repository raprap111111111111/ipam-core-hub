from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend:
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(User.USERNAME_FIELD)

        if email is None or password is None:
            return None

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

User = get_user_model()

class EmailBackend(ModelBackend): # <--- Inherit from ModelBackend
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(User.USERNAME_FIELD)

        if email is None or password is None:
            return None

        try:
            # Good call on iexact, makes it case-insensitive!
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None

        # self.user_can_authenticate(user) is the standard way to check is_active
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None