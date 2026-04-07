from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import time
from companies.models import Company, Branch, Department, Designation, Shift

class Command(BaseCommand):
    help = "Seeder: Companies, Branches, Departments, Designations, and Shifts"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Cleaning up existing corporate data..."))
        Company.objects.all().delete() # Cascades to Branch, Dept, etc.

        # Define the structure for the 4 specific companies
        corporate_structure = [
            {
                "name": "CoreHub Solutions Inc.",
                "code": "CHB",
                "branches": ["Makati HQ", "Cebu Office"],
                "departments": ["Executive", "Information Technology", "Human Resources"],
                "designations": ["Chief Executive Officer", "Senior Developer", "HR Manager"]
            },
            {
                "name": "Total Productivity Inc.",
                "code": "TPI",
                "branches": ["QC Branch", "Davao Site"],
                "departments": ["Operations", "Customer Support"],
                "designations": ["Operations Manager", "Support Lead"]
            },
            {
                "name": "Global Logistics Corp.",
                "code": "GLC",
                "branches": ["Manila Port", "Subic Hub"],
                "departments": ["Logistics", "Warehouse"],
                "designations": ["Fleet Manager", "Inventory Clerk"]
            },
            {
                "name": "Creative Media Agency",
                "code": "CMA",
                "branches": ["BGC Studio"],
                "departments": ["Creative", "Marketing"],
                "designations": ["Art Director", "Social Media Manager"]
            },
        ]

        for data in corporate_structure:
            # 1. Create Company
            company = Company.objects.create(
                name=data["name"],
                code=data["code"],
                registration_number=f"SEC-{data['code']}-2024",
                address="Philippines",
                website=f"https://www.{data['code'].lower()}.com"
            )

            # 2. Create Branches
            for b_name in data["branches"]:
                branch = Branch.objects.create(
                    company=company,
                    name=b_name,
                    code=f"{company.code}-{b_name[:3].upper()}"
                )

                # 3. Create 2 Shifts for every Branch
                Shift.objects.create(
                    branch=branch, 
                    name="Day Shift", 
                    time_in=time(8, 0), 
                    time_out=time(17, 0)
                )
                Shift.objects.create(
                    branch=branch, 
                    name="Night Shift", 
                    time_in=time(22, 0), 
                    time_out=time(7, 0)
                )

                # 4. Create Departments for every Branch
                for d_name in data["departments"]:
                    dept = Department.objects.create(
                        branch=branch,
                        name=d_name,
                        code=f"{branch.code}-{d_name[:3].upper()}"
                    )

                    # 5. Create Designations for every Department
                    for des_name in data["designations"]:
                        Designation.objects.create(
                            department=dept,
                            name=des_name,
                            code=f"{dept.code}-{des_name[:2].upper()}"
                        )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded:\n"
            f"- {Company.objects.count()} Companies\n"
            f"- {Branch.objects.count()} Branches\n"
            f"- {Department.objects.count()} Departments\n"
            f"- {Designation.objects.count()} Designations\n"
            f"- {Shift.objects.count()} Shifts"
        ))