from .models import Employee


class EmployeeService:
    @staticmethod
    def list_employees():
        return Employee.objects.select_related(
            'company',
            'branch',
            'department',
            'designation',
            'shift',
            'employee_status',
            'employee_type',
            'user',
        )

    @staticmethod
    def create_employee(data):
        return Employee.objects.create(**data)