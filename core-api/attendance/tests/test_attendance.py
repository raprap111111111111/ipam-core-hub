from .models import Attendance


class AttendanceService:
    @staticmethod
    def list_attendance():
        return Attendance.objects.select_related('employee')

    @staticmethod
    def create_attendance(data):
        return Attendance.objects.create(**data)