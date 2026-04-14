from rest_framework import serializers
from companies.models import Company, Branch
from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(required=False)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False)
    profile_photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        
        if ret.get('profile_photo'):
            # If DRF didn't already make it an absolute URL, build it manually
            if not ret['profile_photo'].startswith(('http', 'https')):
                if request is not None:
                    ret['profile_photo'] = request.build_absolute_uri(ret['profile_photo'])
                else:
                    # Fallback for local development if request context is missing
                    ret['profile_photo'] = f"http://localhost:8000{ret['profile_photo']}"
        else:
            # Fallback to default avatar if no photo exists
            ret['profile_photo'] = "https://res.cloudinary.com/du2ileegf/image/upload/v1/default-avatar.png"
            
        return ret