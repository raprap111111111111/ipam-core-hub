from rest_framework import serializers


class DashboardEmployeeSerializer(serializers.Serializer):
    total = serializers.IntegerField()


class DashboardAttendanceSerializer(serializers.Serializer):
    present = serializers.IntegerField()


class DashboardLeaveRequestSerializer(serializers.Serializer):
    pending = serializers.IntegerField()


class DashboardRolesSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    primary = serializers.CharField()
    list = serializers.ListField(child=serializers.CharField())


class DashboardProfileSerializer(serializers.Serializer):
    initials = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    account_id = serializers.CharField()
    company_id = serializers.IntegerField(allow_null=True)
    employee_id = serializers.IntegerField(allow_null=True)
    role = serializers.CharField()


class DashboardQuickActionSerializer(serializers.Serializer):
    label = serializers.CharField()
    route = serializers.CharField()


class DashboardRecentActivitySerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class DashboardSummarySerializer(serializers.Serializer):
    employees = DashboardEmployeeSerializer()
    attendance = DashboardAttendanceSerializer()
    leave_requests = DashboardLeaveRequestSerializer()
    roles = DashboardRolesSerializer()
    profile = DashboardProfileSerializer()
    quick_actions = DashboardQuickActionSerializer(many=True)
    recent_activity = DashboardRecentActivitySerializer(many=True)

    # ADD THESE TWO FIELDS:
    permissions = serializers.ListField(child=serializers.CharField())
    sidebar = serializers.ListField(child=serializers.DictField())