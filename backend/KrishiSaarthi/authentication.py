"""Dispatch legacy tokens and expiring Knox tokens without swallowing auth failures."""
from knox.auth import TokenAuthentication as KnoxAuthentication
from rest_framework.authentication import TokenAuthentication


class CompatibleTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        if len(key) == 40:  # Legacy DRF token length; Knox uses 64 characters.
            return super().authenticate_credentials(key)
        return KnoxAuthentication().authenticate_credentials(key.encode('utf-8'))
