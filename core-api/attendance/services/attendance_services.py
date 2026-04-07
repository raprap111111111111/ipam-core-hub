from django.shortcuts import get_object_or_404 # Added this import
from attendance.models import Attendance
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

    @staticmethod # Fixed indentation here
    def get_attendance(pk):
        # This fetches a single record or returns a 404 error if not found
        return get_object_or_404(Attendance, pk=pk)

    @staticmethod
    def update_attendance(pk, data):
        attendance = AttendanceService.get_attendance(pk)
        # Add your update logic here or use a serializer
        for attr, value in data.items():
            setattr(attendance, attr, value)
        attendance.save()
        return attendance

    @staticmethod
    def delete_attendance(pk):
        attendance = AttendanceService.get_attendance(pk)
        attendance.delete()

    @staticmethod
    def check_in_logic(employee, status='present'):
        today = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={'check_in': timezone.now().time(), 'status': status}
        )
        return attendance