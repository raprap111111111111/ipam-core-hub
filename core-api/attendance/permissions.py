from rest_framework import permissions

class IsAttendanceOwner(permissions.BasePermission):
    """User can only see their own clock-in history."""
    def has_object_permission(self, request, view, obj):
        return obj.employee.user == request.user

class CanApproveAttendance(permissions.BasePermission):
    """Only managers or HR can approve attendance logs."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['MANAGER', 'HR']).exists()