from django.contrib import admin
from .models import Employee, EmployeeStatus, EmployeeType

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # This makes the list view look like a real HR dashboard
    list_display = ('employee_id', 'first_name', 'last_name', 'designation', 'employee_status')
    search_fields = ('first_name', 'last_name', 'employee_id')
    list_filter = ('company', 'branch', 'employee_status')

admin.site.register(EmployeeStatus)
admin.site.register(EmployeeType)