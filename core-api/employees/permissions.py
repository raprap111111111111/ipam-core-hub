from rest_framework import permissions

class CanManageEmployees(permissions.BasePermission):
    """
    Check if user is Super Admin or has the MANAGER role.
    """
    def has_permission(self, request, view):
        # 1. Superuser always has access
        if request.user.is_superuser:
            return True
            
        # 2. Maria has "MANAGER" in her roles list
        # We check for both Groups (Django default) and Roles (Your custom setup)
        user_roles = getattr(request.user, 'roles', [])
        is_manager = 'MANAGER' in user_roles or request.user.groups.filter(name='MANAGER').exists()
        
        if request.method in permissions.SAFE_METHODS:
            return True # Anyone authenticated can view list
            
        return is_manager

class IsEmployeeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        # Managers can see employees in their same company
        user_roles = getattr(request.user, 'roles', [])
        if 'MANAGER' in user_roles and obj.company_id == request.user.company_id:
            return True
        # Otherwise, only the owner can see it
        return obj.user == request.user