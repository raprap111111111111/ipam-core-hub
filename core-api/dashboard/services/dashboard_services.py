from itertools import chain
from django.utils import timezone
from employees.models import Employee
from attendance.models import Attendance

class DashboardService:
    @staticmethod
    def _get_sidebar_items(permissions):
        all_items = [
            {
                "label": "Dashboard",
                "icon": "home",
                "path": "/dashboard",
                "permission": "dashboard.view",
            },
            {
                "label": "Employees",
                "icon": "users",
                "path": "/employees",
                "permission": "employees.view",
            },
            {
                "label": "Companies",
                "icon": "building",
                "path": "/companies",
                "permission": "companies.view",
            },
            {
                "label": "Attendance",
                "icon": "clock",
                "path": "/attendance",
                "permission": "attendance.view",
            },
            {
                "label": "Leaves",
                "icon": "calendar",
                "path": "/leaves",
                "permission": "leaves.view",
            },
            {
                "label": "Roles & Permissions",
                "icon": "shield",
                "path": "/roles",
                "permission": "roles.view",
            },
            {
                "label": "Settings",
                "icon": "settings",
                "path": "/settings",
                "permission": "settings.view",
            },
        ]

        return [
            {
                "label": item["label"],
                "icon": item["icon"],
                "path": item["path"],
            }
            for item in all_items
            if item["permission"] in permissions
        ]
        
    @staticmethod
    def get_summary(user):
        roles = DashboardService._get_user_roles(user)
        # Fixed: Changed self to DashboardService and user_roles to roles
        permissions = DashboardService._get_permissions_from_roles(roles)
        sidebar = DashboardService._get_sidebar_items(permissions)

        return {
            "employees": {
                "total": DashboardService._get_employee_total(user, roles),
            },
            "attendance": {
                "present": DashboardService._get_present_today(user, roles),
            },
            "leave_requests": {
                "pending": 0, # Placeholder for leave request logic
            },
            "roles": {
                "count": len(roles),
                "primary": roles[0] if roles else "",
                "list": roles,
            },
            "profile": {
                "initials": DashboardService._get_initials(user),
                "full_name": DashboardService._get_full_name(user),
                "email": getattr(user, "email", "") or "",
                "account_id": str(getattr(user, "id", "") or ""),
                "company_id": DashboardService._get_company_id(user),
                "employee_id": DashboardService._get_employee_id(user),
                "role": roles[0] if roles else "",
            },
            "permissions": permissions,
            "sidebar": sidebar,
            "quick_actions": DashboardService._get_quick_actions(roles),
            "recent_activity": DashboardService._get_recent_activity(user, roles),
        }

    @staticmethod
    def _get_user_roles(user):
        roles = []
        if getattr(user, "is_superuser", False):
            roles.append("superadmin")
            
        # Using .values_list for performance
        user_groups = user.groups.values_list("name", flat=True)
        group_names = [name.lower() for name in user_groups]

        if "hr_admin" in group_names:
            roles.append("hr_admin")
        if "manager" in group_names:
            roles.append("manager")
        
        if hasattr(user, "employee_profile") or "employee" in group_names:
            roles.append("employee")

        return roles

    @staticmethod
    def _get_full_name(user):
        parts = [
            getattr(user, "first_name", ""),
            getattr(user, "middle_name", ""),
            getattr(user, "last_name", ""),
        ]
        full_name = " ".join(str(part).strip() for part in parts if part)
        return full_name or getattr(user, "email", "")

    @staticmethod
    def _get_initials(user):
        first = (getattr(user, "first_name", "") or "")[:1]
        last = (getattr(user, "last_name", "") or "")[:1]
        return f"{first}{last}".upper()

    @staticmethod
    def _get_employee_id(user):
        employee_profile = getattr(user, "employee_profile", None)
        return getattr(employee_profile, "id", "") if employee_profile else ""

    @staticmethod
    def _get_company_id(user):
        employee_profile = getattr(user, "employee_profile", None)
        return getattr(employee_profile, "company_id", "") if employee_profile else ""

    @staticmethod
    def _get_branch_id(user):
        employee_profile = getattr(user, "employee_profile", None)
        return getattr(employee_profile, "branch_id", "") if employee_profile else ""

    @staticmethod
    def _get_scoped_employees(user, roles):
        queryset = Employee.objects.all()
        company_id = DashboardService._get_company_id(user)
        branch_id = DashboardService._get_branch_id(user)
        employee_profile = getattr(user, "employee_profile", None)

        if "superadmin" in roles:
            return queryset
        if "hr_admin" in roles:
            return queryset.filter(company_id=company_id) if company_id else queryset.none()
        if "manager" in roles:
            return queryset.filter(branch_id=branch_id) if branch_id else queryset.none()
        if "employee" in roles:
            return queryset.filter(id=employee_profile.id) if employee_profile else queryset.none()
        
        return queryset.none()

    @staticmethod
    def _get_employee_total(user, roles):
        return DashboardService._get_scoped_employees(user, roles).count()

    @staticmethod
    def _get_present_today(user, roles):
        today = timezone.localdate()
        scoped_employees = DashboardService._get_scoped_employees(user, roles)
        return Attendance.objects.filter(
            employee__in=scoped_employees,
            date=today,
            status__iexact="present",
        ).count()

    @staticmethod
    def _get_quick_actions(roles):
        actions = []
        if any(r in roles for r in ["superadmin", "hr_admin"]):
            actions.append({"label": "Add Employee", "route": "/employees/create"})
        if any(r in roles for r in ["superadmin", "hr_admin", "manager"]):
            actions.append({"label": "Attendance", "route": "/attendance"})
        
        if not actions:
            actions.append({"label": "My Attendance", "route": "/attendance"})
        return actions

    @staticmethod
    def _get_recent_activity(user, roles, limit=5):
        scoped_employees = DashboardService._get_scoped_employees(user, roles)

        attendance_qs = Attendance.objects.filter(
            employee__in=scoped_employees
        ).select_related("employee").order_by("-date", "-id")[:limit]

        return [
            {
                "title": DashboardService._get_employee_name(item.employee),
                "description": DashboardService._format_attendance_activity(item),
            }
            for item in attendance_qs
        ]

    @staticmethod
    def _get_employee_name(employee):
        if not employee: return "Employee"
        return f"{employee.first_name} {employee.last_name}".strip() or "Employee"

    @staticmethod
    def _format_attendance_activity(attendance):
        check_in = getattr(attendance, "check_in", None)
        status = getattr(attendance, "status", "") or ""

        if check_in and hasattr(check_in, "strftime"):
            return f"Clocked in at {check_in.strftime('%I:%M %p')}"
        
        return f"Attendance: {status.title()}" if status else "Activity recorded"
    
    @staticmethod
    def _get_permissions_from_roles(roles):
        role_permission_map = {
            "superadmin": [
                "dashboard.view",
                "employees.view",
                "companies.view",
                "attendance.view",
                "leaves.view",
                "roles.view",
                "settings.view",
            ],
            "hr_admin": [
                "dashboard.view",
                "employees.view",
                "companies.view",
                "attendance.view",
                "leaves.view",
                "settings.view",
            ],
            "manager": [
                "dashboard.view",
                "employees.view",
                "attendance.view",
                "leaves.view",
            ],
            "employee": [
                "dashboard.view",
                "attendance.view",
                "leaves.view",
            ],
        }

        permissions = set()

        for role in roles:
            for permission in role_permission_map.get(role, []):
                permissions.add(permission)

        return sorted(list(permissions))