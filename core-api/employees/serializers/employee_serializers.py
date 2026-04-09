from rest_framework import serializers
from companies.models import Company, Branch
from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    # We explicitly set these to required=False so the API doesn't complain
    employee_id = serializers.CharField(required=False)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False)
    profile_photo = serializers.ImageField(required=False, allow_null=True)


    class Meta:
        model = Employee
        fields = '__all__' # Or your long list of fields
        read_only_fields = ('id', 'created_at', 'updated_at')

    def to_representation(self, instance):
        """Custom representation to handle empty images gracefully"""
        ret = super().to_representation(instance)
        if not ret.get('profile_photo'):
            # You can point this to a generic avatar URL on Cloudinary
            ret['profile_photo'] = "https://res.cloudinary.com/du2ileegf/image/upload/v1/default-avatar.png"
        return ret