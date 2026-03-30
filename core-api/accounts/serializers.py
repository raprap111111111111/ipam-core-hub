from django.contrib.auth import authenticate, password_validation, get_user_model
from rest_framework import serializers

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('User account is inactive.')

        attrs['user'] = user
        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Old password is incorrect.'})
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})

        password_validation.validate_password(attrs.get('new_password'), user=user)
        return attrs

class UserMeSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    account_id = serializers.ReadOnlyField(source='id')
    company_id = serializers.SerializerMethodField()
    employee_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'middle_name', 'last_name',
            'account_id', 'company_id', 'employee_id', 
            'is_staff', 'is_superuser', 'roles', 'permissions'
        ]

    def get_company_id(self, obj):
        return getattr(getattr(obj, 'employee_profile', None), 'company_id', None)

    def get_employee_id(self, obj):
        return getattr(getattr(obj, 'employee_profile', None), 'id', None)

    def get_roles(self, obj):
        if obj.is_superuser: return ["superadmin"]
        return list(obj.groups.values_list('name', flat=True))

    def get_permissions(self, obj):
        if obj.is_superuser: return ["*"]
        return sorted(list(obj.get_all_permissions()))