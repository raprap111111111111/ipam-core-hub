from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Allows access only to users with the Admin role or is_staff."""
    def hasattr_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class IsAccountOwner(permissions.BasePermission):
    """Allows users to only access their own data."""
    def has_object_permission(self, request, view, obj):
        # This checks if the object being accessed IS the user requesting it
        return obj == request.user