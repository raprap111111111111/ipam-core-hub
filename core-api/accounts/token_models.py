import hashlib
import secrets
from django.conf import settings
from django.db import models
from django.utils import timezone


class AccessToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='access_tokens'
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    token_hash = models.CharField(max_length=128, unique=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    revoked_at = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def generate_token(cls):
        raw_token = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        return raw_token, token_hash

    @property
    def is_revoked(self):
        return self.revoked_at is not None

    @property
    def is_expired(self):
        return self.expires_at is not None and timezone.now() >= self.expires_at

    def revoke(self):
        self.revoked_at = timezone.now()
        self.save(update_fields=['revoked_at', 'updated_at'])

    def __str__(self):
        return f"{self.user.email} - {self.name or 'token'}"