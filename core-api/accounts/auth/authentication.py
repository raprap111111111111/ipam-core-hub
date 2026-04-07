import hashlib
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models import AccessToken


class DatabaseTokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != self.keyword:
            raise AuthenticationFailed('Invalid Authorization header format.')

        raw_token = parts[1]
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        try:
            token = AccessToken.objects.select_related('user').get(token_hash=token_hash)
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if token.is_revoked:
            raise AuthenticationFailed('Token has been revoked.')

        if token.is_expired:
            raise AuthenticationFailed('Token has expired.')

        token.last_used_at = timezone.now()
        token.save(update_fields=['last_used_at', 'updated_at'])

        return (token.user, token)