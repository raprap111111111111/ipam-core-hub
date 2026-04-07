from employees.models import Employee


class EmployeeService:
    @staticmethod
    def list_employees():
        return Employee.objects.select_related(
            'company',
            'branch',
            'department',
            'designation',
            'shift',
            # 'employee_status',
            # 'employee_type',
            'user',
        )

    @staticmethod
    def create_employee(data):
        return Employee.objects.create(**data)

    @staticmethod
    def update_employee(employee_instance, data):
        # Helper for your PUT/PATCH requests
        for attr, value in data.items():
            setattr(employee_instance, attr, value)
        employee_instance.save()
        return employee_instance