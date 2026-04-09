import uuid
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

# Models
from companies.models import Company, Branch, Department, Designation, Shift
from employees.models import Employee, EmployeeStatus, EmployeeType

User = get_user_model()

class Command(BaseCommand):
    help = "Seeder: Dedicated Employee Seeder with 7 specific users"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Cleaning up existing Employees and Users..."))
        Employee.objects.all().delete()
        User.objects.all().delete() 

        # 1. SETUP ROLES
        superadmin_role, _ = Group.objects.get_or_create(name='superadmin')
        hr_admin_role, _ = Group.objects.get_or_create(name='HR_ADMIN')
        manager_role, _ = Group.objects.get_or_create(name='MANAGER')
        employee_role, _ = Group.objects.get_or_create(name='EMPLOYEE')

        # 2. SETUP STATUS & TYPES (Required because these are now ForeignKeys)
        status_active, _ = EmployeeStatus.objects.get_or_create(name="active")
        status_on_leave, _ = EmployeeStatus.objects.get_or_create(name="on_leave")
        
        type_regular, _ = EmployeeType.objects.get_or_create(name="regular")
        type_probationary, _ = EmployeeType.objects.get_or_create(name="probationary")

        # 3. FETCH EXISTING CORPORATE STRUCTURE
        companies = list(Company.objects.all())
        branches = list(Branch.objects.all())
        depts = list(Department.objects.all())
        roles = list(Designation.objects.all())
        shifts = list(Shift.objects.all())

        if not companies:
            self.stdout.write(self.style.ERROR("❌ No Companies found! Run your Company seeder first."))
            return

        # 4. YOUR EXACT EMPLOYEE LIST
        employee_list = [
            {"email": "ralph@corehub.com", "first": "Ralph", "middle": "D.", "last": "Admin", "role": superadmin_role, "is_staff": True, "is_superuser": True, "comp_idx": 0},
            {"email": "maria@corehub.com", "first": "Maria", "middle": "S.", "last": "Santos", "role": manager_role, "is_staff": False, "is_superuser": False, "comp_idx": 0},
            {"email": "juan@tpi.com", "first": "Juan", "middle": "P.", "last": "Dela Cruz", "role": employee_role, "is_staff": False, "is_superuser": False, "comp_idx": 1},
            {"email": "elena@tpi.com", "first": "Elena", "middle": "M.", "last": "Gomez", "role": employee_role, "is_staff": False, "is_superuser": False, "comp_idx": 1},
            {"email": "miguel@glc.com", "first": "Miguel", "middle": "A.", "last": "Reyes", "role": employee_role, "is_staff": False, "is_superuser": False, "comp_idx": 2},
            {"email": "sarah@cma.com", "first": "Sarah", "middle": "L.", "last": "Lee", "role": employee_role, "is_staff": False, "is_superuser": False, "comp_idx": 3},
            {"email": "jose@cma.com", "first": "Jose", "middle": "T.", "last": "Rizal", "role": employee_role, "is_staff": False, "is_superuser": False, "comp_idx": 3},
        ]

        self.stdout.write(f"Creating {len(employee_list)} Employees...")

        for i, data in enumerate(employee_list):
            idx = data["comp_idx"] if data["comp_idx"] < len(companies) else 0
            
            # --- USER CREATION ---
            if data["is_superuser"]:
                user = User.objects.create_superuser(
                    email=data["email"],
                    first_name=data["first"],
                    middle_name=data["middle"],
                    last_name=data["last"],
                    password="password123"
                )
            else:
                user = User.objects.create_user(
                    email=data["email"],
                    first_name=data["first"],
                    middle_name=data["middle"],
                    last_name=data["last"],
                    is_staff=data["is_staff"],
                    is_superuser=False,
                    password="password123"
                )
            
            user.groups.add(data["role"])

            # --- EMPLOYEE PROFILE CREATION ---
            Employee.objects.create(
                user=user,
                company=companies[idx],
                branch=branches[idx] if idx < len(branches) else branches[0],
                department=depts[idx] if idx < len(depts) else depts[0],
                designation=roles[idx] if idx < len(roles) else roles[0],
                shift=shifts[idx] if idx < len(shifts) else shifts[0],
                
                employee_id=f"EMP-{str(user.id)[:8]}".upper(),
                first_name=data["first"],
                middle_name=data["middle"],
                last_name=data["last"],
                email=data["email"],
                
                gender="male" if data["first"] not in ["Maria", "Elena", "Sarah"] else "female",
                
                # FIXED: Passing model instances instead of strings
                employee_status=status_active,
                employee_type=type_regular if i % 2 == 0 else type_probationary,
                
                date_of_birth=date(1990 + i, 1, 1),
                phone_number=f"0917-000-000{i}",
                address="Metro Manila, Philippines",
                hired_at=timezone.now().date(),
                
                tax_id=f"123-456-78{i}-000",
                sss_no=f"34-1234567-{i}",
                philhealth_no=f"12-345678901-{i}",
                pagibig_no=f"1212-3434-000{i}",
                
                bank_name="BDO Unibank",
                bank_account_name=f"{data['first']} {data['last']}",
                bank_account_number=f"00123456789{i}"
            )

        self.stdout.write(self.style.SUCCESS(f"🚀 Successfully seeded {len(employee_list)} employees!"))