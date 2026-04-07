from companies.models import Company, Department, Branch, Designation

class CompanyService:
    @staticmethod
    def list_companies():
        return Company.objects.all()

    @staticmethod
    def create_company(data):
        return Company.objects.create(**data)

    @staticmethod
    def get_company(pk):
        return Company.objects.get(pk=pk)

    @staticmethod
    def update_company(pk, data):
        company = Company.objects.get(pk=pk)
        for attr, value in data.items():
            setattr(company, attr, value)
        company.save()
        return company

    @staticmethod
    def delete_company(pk):
        company = Company.objects.get(pk=pk)
        company.delete()

class DepartmentService:
    @staticmethod
    def list_departments():
        return Department.objects.all()

    @staticmethod
    def get_department(pk):
        return Department.objects.get(pk=pk)

    @staticmethod
    def create_department(data):
        return Department.objects.create(**data)

class BranchService:
    @staticmethod
    def list_branches():
        return Branch.objects.all()

    @staticmethod
    def get_branch(pk):
        return Branch.objects.get(pk=pk)

    @staticmethod
    def create_branch(data):
        return Branch.objects.create(**data)

class DesignationService:
    @staticmethod
    def list_designations():
        return Designation.objects.all()

    @staticmethod
    def get_designation(pk):
        return Designation.objects.get(pk=pk)

    @staticmethod
    def create_designation(data):
        return Designation.objects.create(**data)