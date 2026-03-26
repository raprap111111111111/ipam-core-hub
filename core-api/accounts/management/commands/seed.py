import uuid
from datetime import time
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Models
from companies.models import Company, Branch, Department, Designation, Shift
from employees.models import Employee, EmployeeStatus, EmployeeType
from attendance.models import Attendance

User = get_user_model()

class Command(BaseCommand):
    help = "Master Seeder: Email-Auth, Roles, Shifts, Employees, and Attendance"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("!!! Resetting Database !!!"))
        # 1. FOOLPROOF CLEANUP
        self.clear_database()

        # 2. SETUP ROLES
        hr_admin_role, _ = Group.objects.get_or_create(name='HR_ADMIN')
        manager_role, _ = Group.objects.get_or_create(name='MANAGER')
        employee_role, _ = Group.objects.get_or_create(name='EMPLOYEE')

        # 3. SEED CORPORATE STRUCTURE
        company = Company.objects.create(name="Core Hub Solutions", code="CHS-01")
        branch = Branch.objects.create(company=company, name="Manila HQ", code="MNL-HQ")
        it_dept = Department.objects.create(branch=branch, name="IT Operations", code="IT-OPS")
        dev_role = Designation.objects.create(department=it_dept, name="Senior Developer", code="SR-DEV")

        # 4. SEED SHIFTS & STATUS
        morning_shift = Shift.objects.create(
            branch=branch,
            name="Morning Shift", 
            time_in=time(9, 0),
            time_out=time(18, 0)
        )
        active_status, _ = EmployeeStatus.objects.get_or_create(name="Active")
        regular_type, _ = EmployeeType.objects.get_or_create(name="Regular")

        self.stdout.write("Seeding 3 Sample Employees...")

        # 5. SEED EMPLOYEES
        employee_list = [
            {
                "email": "ralph@corehub.com",
                "first": "Ralph",
                "middle": "D.",
                "last": "Admin",
                "role": hr_admin_role,
                "is_staff": True,
                "is_hr": True,
            },
            {
                "email": "maria@corehub.com",
                "first": "Maria",
                "middle": "S.",
                "last": "Santos",
                "role": manager_role,
                "is_staff": False,
                "is_hr": False,
            },
            {
                "email": "juan@corehub.com",
                "first": "Juan",
                "middle": "P.",
                "last": "Dela Cruz",
                "role": employee_role,
                "is_staff": False,
                "is_hr": False,
            },
        ]

        for data in employee_list:
            # --- FIXED INDENTATION START ---
            user = User.objects.create_user(
                email=data["email"],
                first_name=data["first"],
                middle_name=data.get("middle"),
                last_name=data["last"],
                is_staff=data["is_staff"],
                is_superuser=data["is_staff"],
                is_hr_admin=data["is_hr"], # Matching your User model
                password="password123"
            )
            user.groups.add(data["role"])

            # Create Employee Profile
            emp = Employee.objects.create(
                user=user,
                company=company,
                branch=branch,
                department=it_dept,
                designation=dev_role,
                shift=morning_shift,
                employee_status=active_status,
                employee_type=regular_type,
                employee_id=f"EMP-{str(user.id)[:8]}".upper(),
                first_name=data["first"],
                last_name=data["last"],
                email=data["email"],
                hired_at=timezone.now().date()
            )

            # Create Attendance
            Attendance.objects.create(
                employee=emp,
                date=timezone.now().date(),
                check_in=timezone.now().time(),
                status='present'
            )
            # --- FIXED INDENTATION END ---

        self.stdout.write(self.style.SUCCESS("🚀 Master Enterprise Seeded Successfully!"))

    def clear_database(self):
        self.stdout.write("Cleaning up existing data...")
        Attendance.objects.all().delete()
        Employee.objects.all().delete()
        User.objects.all().delete() 
        Group.objects.all().delete()
        Shift.objects.all().delete()
        Designation.objects.all().delete()
        Department.objects.all().delete()
        Branch.objects.all().delete()
        Company.objects.all().delete()
        EmployeeStatus.objects.all().delete()
        EmployeeType.objects.all().delete()