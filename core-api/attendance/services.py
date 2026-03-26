from .models import Attendance
from django.utils import timezone

class AttendanceService:
    @staticmethod
    def list_attendance():
        # Added select_related to make the API faster
        return Attendance.objects.select_related('employee').all()

    @staticmethod
    def create_attendance(data):
        # This handles the POST request from the view
        return Attendance.objects.create(**data)

    @staticmethod
    def check_in_logic(employee, status='present'):
        # Your existing logic for automatic check-in
        today = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={'check_in': timezone.now().time(), 'status': status}
        )
        return attendance