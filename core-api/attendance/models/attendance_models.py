from django.db import models
from employees.models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True) # Note: TimeField only stores HH:MM:SS
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='present')

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.date}"