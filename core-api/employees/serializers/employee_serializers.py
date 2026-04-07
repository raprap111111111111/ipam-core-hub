from rest_framework import serializers
from companies.models import Company, Branch
from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    # We explicitly set these to required=False so the API doesn't complain
    employee_id = serializers.CharField(required=False)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False)

    class Meta:
        model = Employee
        fields = '__all__' # Or your long list of fields