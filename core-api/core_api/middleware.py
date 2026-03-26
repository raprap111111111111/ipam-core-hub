from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied

class InstantLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We only care about API requests
        if request.path.startswith('/api/'):
            try:
                # Try to authenticate the user from the header
                auth = JWTAuthentication().authenticate(request)
                if auth is not None:
                    user, token = auth
                    # If you blacklisted the token's JTI, this will fail
                    # Or you can add a custom "is_logged_out" check here
            except:
                pass 
        return self.get_response(request)