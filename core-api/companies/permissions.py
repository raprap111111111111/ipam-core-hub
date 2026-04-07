from rest_framework import permissions

class IsCompanyAdmin(permissions.BasePermission):
    """
    Super Admin sees all. 
    Others can only see/edit their own Company.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        # Ensure user is linked to the company they are trying to access
        return request.user.company == obj

class BelongsToCompany(permissions.BasePermission):
    """Checks if the user belongs to the company."""
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user.company == obj