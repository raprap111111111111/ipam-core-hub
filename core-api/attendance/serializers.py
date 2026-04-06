from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    # This creates a custom field that combines the employee's first and last name
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        
        # Adding 'employee_name' to the existing fields
        fields = [
            'id', 
            'employee',   
            'employee_name',
            'date', 
            'check_in', 
            'check_out', 
            'status'
        ]

    def get_employee_name(self, obj):
        # Accesses the related Employee model via the ForeignKey
        return f"{obj.employee.first_name} {obj.employee.last_name}"